# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

import numpy as np

class Material:
    def __init__(self):
        self.elements = {}

    def __init__(self, materialElements):
        self.elements = materialElements

    def AddElement(self,elementName,proportion):
        self.elements[elementName] = proportion

    def CalculateActivation(self):
        for 

class AllActivationData:
    def __init__(self):
