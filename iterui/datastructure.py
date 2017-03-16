# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

import numpy as np

class AllActivationData:
    def __init__(self):
        #6 activity, dose rate, heat, ingestion dose, #6 spectrums
        self.activity = []
        self.dose = []
        self.heat = []
        self.idose = []
        self.spectrum = []

    def __init__(self,activationFileName):

    def LoadFromFile(self,activationFileName):
        #读取活化数据
        #读取核素演变数据


class Material:
    def __init__(self):
        self.elements = {}
        self.activationdata = AllActivationData()

    def __init__(self, ielements):
        self.elements = ielements

    def AddElement(self,elementName,proportion):
        if("elementName" in self.elements):
            self.elements[elementName] = self.elements[elementName] + proportion
        else:
            self.elements[elementName] = proportion

    def CalculateActivation(self):
        propSum = 0.0
        for name,prop in self.elements.items():
            propSum += prop
        for name,prop in self.elements.items():
            propSum += prop

class Element(Material):
    def __init__(self,name):
        super(Element,self).__init__(self)
        self.elements[name] = 1.0;
        if(not self.AllActivationData.LoadFromFile(name+".out")):
            self.valid = False
        else:
            self.valid = True

class ElementPool:
    def __init__(self):
        self.elementPool = {}

    def GetElement(self,name):
        if(name in self.elementPool):
            return self.elementPool[name]
        self.elementPool[name] = Element(name)

class PathWayAnalysis:
    def __init__(self):
        self._targetNuclideName = 'N/A'
        self._pathWay = ''
        self._prop = 0.0