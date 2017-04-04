# -*- coding: utf-8 -*-

import re
import copy


class BaseData:
    def __mul__(self, number):
        new_data = copy.deepcopy(self)
        new_data *= number
        return new_data

    def __add__(self, other):
        new_data = copy.deepcopy(self)
        new_data += other
        return new_data



class MaterialPathWays(BaseData):
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

    def normalize(self):
        for key, val in self.all_path_ways.items():
            val.normalize()

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
                    new_path_way.read_raw_lines(lines, i)
                    self.all_path_ways[new_path_way.target_nuclide] = new_path_way
                except Exception:
                    next
        return True

    def output(self):
        for key, val in self.all_path_ways.items():
            print(key)
            for key2,val2 in val.pathway.items():
                print("{0}:{1}".format(key2,val2))

    def __imul__(self, factor):
        for key, val in self.all_path_ways.items():
            val *= factor
        return self

    # seem to be continued
    def __iadd__(self, other):
        for key, val in other.all_path_ways.items():
            if key in self.all_path_ways:
                self.all_path_ways[key] += val
            else:
                self.all_path_ways[key] = val
        return self


class PathWay(BaseData):
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

    def normalize(self):
        sum_prop = 0.0
        for key, val in self.pathway.items():
            sum_prop += val
        for key, val in self.pathway.items():
            self.pathway[key] = val*100/sum_prop

    def read_raw_lines(self,lines,start_idx):
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
                pathway_str.strip('\r\n ')
                percent = eval(percent_part[percent_part.rfind(' '):])
                self.pathway[pathway_str] = percent
                number_target = number_target-1
            if number_target == 0:
                break
            if (lines[i].startswith(' Target nuclide')
                or lines[i].find('G E N E R I C   P A T H W A Y S') > 0):
                raise Exception('path way format error, path number incompact for ', self.target_nuclide)
        return True

    def __imul__(self, factor):
        for key, val in self.pathway.items():
            self.pathway[key] *= factor
        return self

    def __iadd__(self, other_pathway):
        assert(self.target_nuclide == other_pathway.target_nuclide)
        for key, val in other_pathway.pathway.items():
            if key in self.pathway:
                self.pathway[key] += other_pathway.pathway[key]
            else:
                self.pathway[key] = other_pathway.pathway[key]
        return self

def functest_pathway():
    lines = []
    with open('C:/Users/ysp/Desktop/QT_practice/ITER DATA/Flux1/Fe/Fe.out') as inputfile:
        lines.extend(inputfile.readlines())
    new_pathways = MaterialPathWays()
    new_pathways.read_raw_lines(lines)
    print('readover')

if __name__ == '__main__':
    functest_pathway()
    print('over')