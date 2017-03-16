# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

import numpy as np

class ElementPool:
    def __init__(self):


class Element:
    def __init__(self,name):
        self._name = name;
        self.AllActivationData


class Material:
    def __init__(self):
        self._elements = {}
        self._activationdata = AllActivationData()

    def __init__(self, elements):
        self._elements = elements

    def AddElement(self,elementName,proportion):
        if("elementName" in self.elments):
            self._elements[elementName] = self._elements[elementName] + proportion
        else:
            self._elements[elementName] = proportion

    def CalculateActivation(self):
        propSum = 0.0
        for name,prop in self._elements.items():
            propSum += prop
        for name,prop in self._elements.items():
            propSum += prop

class AllActivationData:
    def __init__(self):
        self._activity = []
        self._
    def __init__(self,activationFileName):

    def LoadFromFile(self,activationFileName):
        #读取活化数据
        #读取核素演变数据

class PathWayAnalysis:
    def __init__(self):
        self._targetNuclideName = 'N/A'
        self._pathWay = ''
        self._prop = 0.0