# -*- coding: utf-8 -*-

import numpy as np

import copy

from data_handling.activationdata import ActivationData
from base.base import *
import pickle

import os

class MaterialListLibrary:
    def __init__(self):
        self.material_list = []
        self.load_material_list()

    def load_material_list(self):
        if os.path.exists(BasicPath.material_list_file_name):
            with open(BasicPath.material_list_file_name) as list_file:
                lines = list_file.readlines()
                for line in lines:
                    line = line.strip('\r\n\s')
                    if len(line) > 0:
                        new_mat = Material(line)
                        self.material_list.append(new_mat)

    def save_material_list(self):
        with open(BasicPath.material_list_file_name, 'w') as list_file:
            for mat in self.material_list:
                list_file.write(mat)


class Material:
    def __init__(self):
        self.elements = dict()
        self.name = ''
        self.activationdata = ActivationData()

    def __init__(self, line):
        elems = [a for a in line.split(' ') if len(a) > 0 and a != '\n']
        if len(elems) % 2 != 1:
            raise YSPException("error, in ")
        self.elements = dict()
        self.name = elems[0]
        for i in range(0, int((len(elems)-1)/2)):
            self.elements[elems[2*i+1]] = elems[2*i+2]

    def add_element(self, element_name,proportion):
        if "elementName" in self.elements:
            self.elements[element_name] = self.elements[element_name] + proportion
        else:
            self.elements[element_name] = proportion

    def calculate_activation(self):
        prop_sum = 0.0
        for name, prop in self.elements.items():
            prop_sum += prop
        for name, prop in self.elements.items():
            prop /= prop_sum
        # to be continued, extra need to be added


class Element(Material):
    def __init__(self,name):
        super(Element,self).__init__(self)
        self.elements[name] = 1.0
        self.name = name
        self.activationdata = ActivationData()
        self.valid = self.activationdata.read_raw_files(self.name)

    def get_restored_file(self):
        return self.name+'.cache'


class ElementPool:
    dict_elems = {}

    @staticmethod
    def get_elem(name):
        if name in ElementPool.dict_elems:
            return ElementPool.dict_elems[name]
        else:
            new_elem = Element(name)



