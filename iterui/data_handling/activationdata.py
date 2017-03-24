# -*- coding: utf-8 -*-


import numpy as np

import copy


class ActivationData:
    def __init__(self):
        # 6 activity, dose rate, heat, ingestion dose, #6 spectrums
        self.activition_data = []

    def __init__(self,fispact_output):
        self.load_file(fispact_output)

    def load_file(self,matname):
        #获得5个文件名
        #读取活化数据
        #读取核素演变数据
        return False

class OneSpectrumActivationData:
    def __init__(self):
        self.allStepsActivationData = []

    def read_data(self,inputfilename):
        lines = []
        opensucessful = False
        try:
            with open(inputfilename) as inputfile:
                lines.extend(inputfile.readlines())
        except IOError:
            opensucessful = False
        else:
            opensucessful = True
            startlinesforsteps = []
            for i in range(0,len(lines)):
                if lines[i].startswith('1* * * * * TIME INTERVAL'):
                    startlinesforsteps.append(i)
            startlinesforsteps.append(len(lines))
            for i in range(1,len(startlinesforsteps)):
                onestepdata = OneSpectrumOneStepActivationData()
                onestepdata.load_from_lines(lines,startlinesforsteps[i-1],startlinesforsteps[i])
                self.allStepsActivationData.append(onestepdata)
        finally:
            return opensucessful

class OneSpectrumOneStepActivationData:
    def __init__(self):
        self.time = 0.0
        self.nuclides = dict() #核素以及原子数比
        self.total_activity = 0.0
        self.total_activity_no_tritium = 0.0
        self.alpha_heat = 0.0
        self.beta_heat = 0.0
        self.gamma_heat = 0.0
        self.total_heat = 0.0
        self.init_mass = 0.0
        self.cur_mass = 0.0
        self.neutron_flux_during_interval = 0.0
        self.number_fission = 0.0
        self.ingestion_harzard = 0.0
        self.inhalation_harzard = 0.0
        self.ingestion_harzard_no_tritium = 0.0
        self.inhalation_harzard_no_tritium = 0.0
        self.gas_rate = 0.0

    def load_from_lines(self,lines,startidx,endidx):
        newlines= lines[startidx:endidx]
        #核素成分
        #总活度等信息

        return True

class PathWay:
    def __init__(self,target_nuclide):
        self.target_nuclide = target_nuclide
        #pathway's key is the whole pathway,
        #the val is the generated nulicdes' weight per kilogram (kg) original material
        self.pathway = dict()

    def add_pathway(self,strpathway,proportion):
        if strpathway in self.pathway:
            self.pathway[strpathway] += proportion
        else:
            self.pathway[strpathway] = proportion

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
            self.add_pathway(key,val)
        return self

    def __add__(self,other_pathway):
        new_path_way = copy.deepcopy(self)
        new_path_way += other_pathway
        return new_path_way