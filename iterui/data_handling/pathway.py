# -*- coding: utf-8 -*-

import re

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
#                    100.00%(n,g)    100.00%(n,g)

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
        # the val is the generated nulicdes' weight per kilogram (kg) original material
        self.pathway = dict()

    def load_raw_lines(self,lines):


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
