# -*- coding: utf-8 -*-


import numpy as np

import copy


class ActivationData:
    def __init__(self):
        # 6 activity, dose rate, heat, ingestion dose, #6 spectrums
        self.activition_data = []

    def __init__(self,fispact_output):
        self.load_file(fispact_output)

    def read_raw_file(self,matname):
        #obtain 5 files
        data_file_names = ['Flux1\\{0}\\{0}.out'.format(matname),
                          'Flux2\\{0}\\{0}.out'.format(matname),
                          'Flux4\\{0}\\{0}.out'.format(matname),
                          'Flux5\\{0}\\{0}.out'.format(matname),
                          'Flux6\\{0}\\{0}.out'.format(matname)]
        for file_name in data_file_names:
            new_one_spectra_data = OneSpectrumActivationData()
            new_one_spectra_data.read_raw_file(file_name)
            self.activition_data.append(new_one_spectra_data)
        #read 5 data files
        return False

    def get_spectra_data(self,spectraidx):
        if spectraidx == 1:
            return self.activition_data[0]
        elif spectraidx == 2:
            return self.activition_data[1]
        elif spectraidx == 3:
            return self.activition_data[2]
        elif spectraidx == 4:
            return self.activition_data[2]
        elif spectraidx == 5:
            return self.activition_data[3]
        elif spectraidx == 6:
            return self.activition_data[4]
        else:
            return None

class OneSpectrumActivationData:
    def __init__(self):
        self.allStepsActivationData = []

    def read_raw_file(self, inputfilename):
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
            for i in range(0, len(lines)):
                if lines[i].startswith('1* * * * * TIME INTERVAL'):
                    startlinesforsteps.append(i)
            startlinesforsteps.append(len(lines))
            #if need to skip previous time steps, need to change the range
            for i in range(1, len(startlinesforsteps)):
                onestepdata = OneSpectrumOneStepActivationData()
                onestepdata.load_from_raw_lines(lines, startlinesforsteps[i-1], startlinesforsteps[i])
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

    def load_from_raw_lines(self, lines, startidx, endidx):
        # nuclides info (first)
        nuclide_data_start_idx = startidx + 4
        nuclide_data_end_idx = nuclide_data_start_idx
        for i in range(nuclide_data_start_idx,endidx):
            if

        # total info

        return True

class OneNuclideData:
    param_names = ['atoms',
                   'weight(g)',
                   'activation(Bq)',
                   'beta_heat(kW)',
                   'alpha_heat(kW)',
                   'gamma_heat(kW)',
                   'dose_rate(Sv)',
                   'ing_dose(Sv)',
                   'inh_dose(Sv)',
                   'Bq/A2_Ratio',
                   'half_life(sec)']
    def __init__(self):
        #  NUCLIDE        ATOMS         GRAMS        Bq       b-Energy    a-Energy   g-Energy    DOSE RATE   INGESTION  INHALATION     Bq/A2     HALF LIFE
        #                                                kW          kW         kW         Sv/hr      DOSE(Sv)    DOSE(Sv)     Ratio      seconds
        self.params = {}
        self.nuclide_name = ''

    def read_raw_line(self,line):
        val_list = [a for a in line.split(' ') if len(a) > 0]
        if len(val_list) == 14:
            del val_list[2]
        if len(val_list) < 13:
            return False
        self.nuclide_name = val_list[0]+val_list[1]
        for i in range(0, len(OneNuclideData.param_names)-1):
            self.params[OneNuclideData.param_names[i]] = eval(val_list[i])
        if val_list[-1] == 'Stable':
            self.params['half_life(sec)'] = -1
        else:
            self.params['half_life(sec)'] = eval(val_list[-1])
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