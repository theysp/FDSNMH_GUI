# -*- coding: utf-8 -*-

import numpy as np

import copy

from activationdata import *


class Material:
    def __init__(self):
        self.elements = dict()
        self.activationdata = ActivationData()

    def __init__(self, input_elements):
        self.elements = input_elements

    def add_element(self,element_name,proportion):
        if "elementName" in self.elements:
            self.elements[element_name] = self.elements[element_name] + proportion
        else:
            self.elements[element_name] = proportion

    def calculate_activation(self):
        prop_sum = 0.0
        for name,prop in self.elements.items():
            prop_sum += prop
        for name,prop in self.elements.items():
            prop /= prop_sum
        # to be continued, extra need to be added

class Element(Material):
    def __init__(self,name):
        super(Element,self).__init__(self)
        self.elements[name] = 1.0
        self.name = name
        self.valid = self.activationdata.load_file(self.get_output_name())

    def get_output_name(self):
        return self.name+'.out'

class ElementPool:
    def __init__(self):
        self.elementPool = {}

    def get_element(self,name):
        if not(name in self.elementPool):
            self.elementPool[name] = Element(name)
        return self.elementPool[name]

