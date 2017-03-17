# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

import numpy as np

import copy

class AllActivationData:
    def __init__(self):
        #6 activity, dose rate, heat, ingestion dose, #6 spectrums
        self.activity = []
        self.dose = []
        self.heat = []
        self.idose = []
        self.spectrum = []

    def __init__(self,fispact_output):
        self.load_file(fispact_output)

    def load_file(self,fispact_output):
        #读取活化数据
        #读取核素演变数据

class Material:
    def __init__(self):
        self.elements = dict()
        self.activation_data = AllActivationData()

    def __init__(self, input_elements):
        self.elements = input_elements

    def add_element(self,element_name,proportion):
        if "elementName" in self.elements:
            self.elements[element_name] = self.elements[element_name] + proportion
        else:
            self.elements[element_name] = proportion

    def calculate_activation(self):
        propSum = 0.0
        for name,prop in self.elements.items():
            propSum += prop
        for name,prop in self.elements.items():
            propSum += prop

class Element(Material):
    def __init__(self,name):
        super(Element,self).__init__(self)
        self.elements[name] = 1.0
        self.name = name
        if not self.activation_data.load_file(self.get_output_name()):
            self.valid = False
        else:
            self.valid = True

    def get_output_name(self):
        return self.name+'.out'

class ElementPool:
    def __init__(self):
        self.elementPool = {}

    def get_element(self,name):
        if name in self.elementPool:
            return self.elementPool[name]
        self.elementPool[name] = Element(name)

class PathWay:
    def __init__(self):
        self.target_nuclide = 'N/A'
        #pathway's key is the whole pathway,
        #the val is the generated nulicdes' weight per kilogram (kg) original material
        self.pathway = dict()

    def __imul__(self,factor):
        for key,val in self.pathway.items():
            self.pathway[key] += self.pathway[key] * factor
        return self

    def __mul__(self,factor):
        new_path_way = copy.deepcopy(self)
        new_path_way *= factor
        return new_path_way

    def __iadd__(self,other_pathway):
        if self.target_nuclide != other_pathway.target_nuclide:
            return False
        for key,val in other_pathway.pathway.items():
            if(key in self.pathway):
                self.pathway[key] += other_pathway.pathway[key]
            else:
                self.pathway[key] = other_pathway.pathway[key]
        return self

    def __add__(self,other_pathway):
        new_path_way = copy.deepcopy(self)
        new_path_way += other_pathway
        return new_path_way