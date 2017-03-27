# -*- coding: utf-8 -*-

import re
import copy


class MaterialPathWays:
    # Example:
    #  Source Nuclides
    #  Fe 54      Fe 56      Fe 57      Fe 58
    #
    # Target Nuclides
    #  Fe 59      Fe 55      Mn 56      Mn 54      Cr 51      Mn 57      Fe 53      Mn 58m     Mn 58      Cr 55
    #  Co 60      H   3      Mn 53      Fe 60
    #
    # Listed below are all significant paths and loops ordered by target nuclide. The first line for each target nuclide gives the nuclide name and the percentage
    # ...
    # Target nuclide Mn 53    100.000% of inventory given by  2 paths
    # --------------------
    #
    # path  1  97.873% Fe 54 ---(R)--- Mn 53 ---(L)---
    #                     96.12%(n,np)
    #                      3.88%(n,d)
    #
    # path  2   2.127% Fe 54 ---(R)--- Fe 53 ---(d)--- Mn 53 ---(L)---
    #                    100.00%(n,2n)   100.00%(b+)
    #
    # Target nuclide Fe 60    100.000% of inventory given by  1 path
    # --------------------
    #
    # path  1 100.000% Fe 58 ---(R)--- Fe 59 ---(r)--- Fe 60 ---(L)---
    #                    100.00%(n,g)      100.00 % (n, g)
    def __init__(self):
        # all_path_ways contains all the pathways for all the target nuclides of this material
        self.all_path_ways = dict()

    def read_raw_lines(self, lines, start_idx=0):
        real_start_idx = -1
        for i in range(start_idx, len(lines)):
            if lines[i].startswith(' Target nuclide '):
                real_start_idx = i
                break
        if real_start_idx < 0:
            raise Exception('read path way failed, cannot find the start of pathway')
        real_end_idx = -1
        for i in range(real_start_idx, len(lines)-1):
            if len(lines[i])<2 and len(lines[i+1]) < 2:
                real_end_idx = i
        if real_end_idx < 0:
            raise Exception('read path way failed, cannot find the start of pathway')
        for i in range(real_start_idx, real_end_idx):
            if lines[i].startswith(' Target nuclide '):
                new_path_way = PathWay('unknown')
                try:
                    new_path_way.load_raw_lines(lines, i)
                    self.all_path_ways[new_path_way.target_nuclide] = new_path_way
                except Exception:
                    next
        return True


class PathWay:
    #  Example1 :
    #  Target nuclide Mn 53    100.000% of inventory given by  2 paths
    # --------------------
    #
    # path  1  97.873% Fe 54 ---(R)--- Mn 53 ---(L)---
    #                     96.12%(n,np)
    #                      3.88%(n,d)
    #
    # path  2   2.127% Fe 54 ---(R)--- Fe 53 ---(d)--- Mn 53 ---(L)---
    #                    100.00%(n,2n)   100.00%(b+)
    def __init__(self, target_nuclide):
        self.target_nuclide = target_nuclide
        # pathway's key is the whole pathway,
        # the val is the percentage
        self.pathway = dict()

    def load_raw_lines(self,lines,start_idx):
        if not lines[start_idx].startswith(' Target nuclide '):
            raise Exception('invalid start of pathway')
        # Target nuclide Mn 53    100.000% of inventory given by  2 paths
        words = [a for a in lines[start_idx].split(' ') if len(a) > 0 and a != '\n']
        if len(words) < 11:
            raise Exception('no enough information in target nuclide line')
        self.target_nuclide = words[2]+' '+words[3]
        number_target = eval(words[9])
        for i in range(start_idx+1, len(lines)-1):
            if lines[i].startswith(' path  '):
                (percent_part, pathway_str) = lines[i].split('%')
                percent = eval(percent_part[percent_part.rfind(' '):])
                self.pathway[pathway_str] = percent
                number_target = number_target-1
            if number_target == 0:
                break
            if (lines[i].startswith(' Target nuclide')
                or lines[i].find('G E N E R I C   P A T H W A Y S') > 0):
                raise Exception('path way format error, path number incompact for ', self.target_nuclide)
        return True

    def add_pathway(self, strpathway, proportion):
        if strpathway in self.pathway:
            self.pathway[strpathway] += proportion
        else:
            self.pathway[strpathway] = proportion

    def __imul__(self, factor):
        for key, val in self.pathway.items():
            self.pathway[key] += self.pathway[key] * factor
        return self

    def __mul__(self, factor):
        new_path_way = copy.deepcopy(self)
        new_path_way *= factor
        return new_path_way

    def __iadd__(self, other_pathway):
        if self.target_nuclide != other_pathway.target_nuclide:
            return False
        for key, val in other_pathway.pathway.items():
            self.add_pathway(key, val)
        return self

    def __add__(self, other_pathway):
        new_path_way = copy.deepcopy(self)
        new_path_way += other_pathway
        return new_path_way

def functest():
    lines = []
    with open('C:/Users/ysp/Desktop/QT_practice/ITER DATA/Flux1/Fe/Fe.out') as inputfile:
        lines.extend(inputfile.readlines())
    new_pathways = MaterialPathWays()
    new_pathways.read_raw_lines(lines)
    print('readover')

if __name__ == '__main__':
    functest()
    print('over')