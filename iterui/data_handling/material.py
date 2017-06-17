# -*- coding: utf-8 -*-

import numpy as np
import copy
from data_handling.activationdata import ActivationData
from base.base import *
import pickle
import os


class MaterialListLibrary:
    def __init__(self):
        self.materials = {}
        self.load_material_list()

    def load_material_list(self):
        if os.path.exists(BasicPath.material_list_file_name):
            with open(BasicPath.material_list_file_name) as list_file:
                lines = list_file.readlines()
                for line in lines:
                    line = line.strip('\r\n\s')
                    if len(line) > 0:
                        new_mat = Material(line)
                        self.materials[new_mat.name] = (new_mat)

    def save_material_list(self):
        with open(BasicPath.material_list_file_name, 'w') as list_file:
            for mat in self.materials.values():
                line = mat.to_string()
                list_file.write(line+'\n')

    def add_material(self,material):
        if material.name in self.materials.keys():
            raise YSPException('material: '+material.name+' already exists, please change material name')
        self.materials[material.name] = material

    def del_material(self, matname):
        if matname in self.materials.keys():
            self.materials.pop(matname)


class Material:
    def __init__(self, line='Empty'):
        name = ''
        elemline = ''
        self.spectrum = ''
        try:
            (name, elemline) = line.split('|')
        except ValueError:
            name = line.strip('\n\r ')
        elems = [a for a in elemline.split(' ') if len(a) > 0 and a != '\n']
        if len(elems) % 2 != 0:
            raise YSPException("error, in ")
        self.elements = dict()
        self.name = name.strip(' ')
        self.activation_data = None
        if len(elems) > 1: # normal material
            for i in range(0, int(len(elems)/2)):
                self.elements[elems[2*i]] = eval(elems[2*i+1])
        elif line != 'Empty' and len(line)>0:              # single elements
            self.elements[self.name] = 100.0

    def add_element(self, element_name,proportion):
        if "elementName" in self.elements:
            self.elements[element_name] = self.elements[element_name] + proportion
        else:
            self.elements[element_name] = proportion

    def normalize(self):
        prop_sum = 0.0
        for name, prop in self.elements.items():
            prop_sum += prop
        for name in self.elements.keys():
            self.elements[name] = self.elements[name] * 100 / prop_sum

    def to_string(self):
        self.normalize()
        line = self.name + ' | '
        for elem, prop in self.elements.items():
            line = line + "{0} {1:.2e} ".format(elem, prop)
        return line

#Here after are for the activation properties of the material under all spectra
    def calculate_activation(self):
        self.normalize()
        # to be continued, extra need to be added
        for element_name in self.elements.keys():
            element = ElementPool.get_elem(element_name)
            if self.activation_data is None:
                self.activation_data = element.activation_data*(self.elements[element_name]/100)
            else:
                self.activation_data += element.activation_data*(self.elements[element_name]/100)
        return True

    def get_cache_file_path(self):
        # hash name
        #line = self.to_string()
        file_name = BasicPath.element_cache_folder +"/{}.mat".format(self.name)
        return file_name

    def cache_material(self):
        try:
            cache_file_path = self.get_cache_file_path()
            if os.path.exists(cache_file_path):
                os.remove(cache_file_path)
            with open(cache_file_path, 'wb') as outfile:
                pickle.dump(self, outfile)
            return True
        except Exception:
            return False

    def get_cached_material(self):
        cache_file_path = self.get_cache_file_path()
        newmat = None
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'rb') as infile:
                newmat = pickle.load(infile)
        return newmat

#Here after are for the activation properties of the material under a specific spectrum
    def calculate_spectrum_activation(self, spectrum_name):
        self.spectrum = spectrum_name
        self.normalize()
        # to be continued, extra need to be added
        for element_name in self.elements.keys():
            element = ElementPool.get_spectrum_elem(element_name, spectrum_name)
            if self.activation_data is None:
                self.activation_data = element.activation_data * (self.elements[element_name] / 100)
            else:
                self.activation_data += element.activation_data * (self.elements[element_name] / 100)
        return True

    def cache_spectrum_material(self,spectrum_name):
        try:
            cache_file_path = self.get_cache_spectrum_file_path()
            if os.path.exists(cache_file_path):
                os.remove(cache_file_path)
            with open(cache_file_path, 'wb') as outfile:
                pickle.dump(self, outfile)
            return True
        except Exception:
            return False

    def get_cache_spectrum_file_path(self,spectrum_name):
        # hash name
        #line = self.to_string()
        file_name = BasicPath.element_cache_folder +"/{}_{}.mat".format(self.name,spectrum_name)
        return file_name

    def get_cached_spectrum_material(self,spectrum_name):
        cache_file_path = self.get_cache_spectrum_file_path(spectrum_name)
        newmat = None
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'rb') as infile:
                newmat = pickle.load(infile)
        return newmat


class Element(Material):
    def __init__(self, name):
        super(Element, self).__init__()
        self.elements[name] = 1.0
        self.name = name
        self.spectrum = ''
        self.activation_data = ActivationData()
        self.valid = self.activation_data.read_raw_files(self.name)

    def __init__(self, name, spectrum_name):
        super(Element, self).__init__()
        self.elements[name] = 1.0
        self.name = name
        self.spectrum = spectrum_name
        self.activation_data = ActivationData()
        self.valid = self.activation_data.read_raw_spectrum_file(self.name,spectrum_name)

    def get_restored_file(self):
        return self.name+'.cache'


class ElementPool:
    dict_elems = {}

    @staticmethod
    def get_elem(name):
        if name in ElementPool.dict_elems:
            return ElementPool.dict_elems[name]
        else:
            # check if there is cache
            new_elem = None
            if os.path.exists(BasicPath.element_cache_folder+'/{0}.cache'.format(name)):
                with open(BasicPath.element_cache_folder+'/{0}.cache'.format(name),'rb') as infile:
                    new_elem = pickle.load(infile)
            else:
                new_elem = Element(name)
                with open(BasicPath.element_cache_folder+'/{0}.cache'.format(name),'wb') as outfile:
                    pickle.dump(new_elem,outfile)
            ElementPool.dict_elems[name] = new_elem
            return new_elem

    @staticmethod
    def get_cache_spectrum_file_path(name, spectrum_name):
        return BasicPath.element_cache_folder+'/{}_{}.cache'.format(name,spectrum_name)

    @staticmethod
    def get_spectrum_elem(name, spectrum_name):
        full_name = name+":"+spectrum_name
        if full_name in ElementPool.dict_elems:
            return ElementPool.dict_elems[full_name]
        else:
            # check if there is cache
            new_elem = None
            cache_file_name = ElementPool.get_cache_spectrum_file_path(name, spectrum_name)
            if os.path.exists(cache_file_name):
                with open(cache_file_name,'rb') as infile:
                    new_elem = pickle.load(infile)
            else:
                new_elem = Element(name, spectrum_name)
                with open(cache_file_name,'wb') as outfile:
                    pickle.dump(new_elem,outfile)
            ElementPool.dict_elems[full_name] = new_elem
            return new_elem


