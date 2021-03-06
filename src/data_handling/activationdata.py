# -*- coding: utf-8 -*-


import numpy as np
import re
import copy
import pickle

from data_handling.pathway import MaterialPathWays
from data_handling.pathway import BaseData
from base.base import *

num_pattern = re.compile('\d+\.?\d+E?[+-]?\d+')


def eval_str_number(num_str):
    new_num_str = num_str
    pos_minus_plus = num_str.find('-')
    if pos_minus_plus < 0:
        pos_minus_plus = num_str.find('+')
    if pos_minus_plus > 0:
        ch_before_minus = num_str[pos_minus_plus - 1]
        if ch_before_minus != 'e' and ch_before_minus != 'E':
            new_num_str = num_str[:pos_minus_plus] + 'E' + num_str[pos_minus_plus:]
    try:
        return eval(new_num_str)
    except Exception:
        return -1.0


class ActivationData(BaseData):

    def __init__(self, raw_name = None):
        self.activation_data = dict()
        if not(raw_name is None):
            self.read_raw_file(raw_name)

    def read_raw_files(self, raw_name):
        # obtain 5 files
        spectra_list = BasicPath.get_spectra_list()
        for spectrum_name in spectra_list:
            data_dir_name = BasicPath.get_spectra_dir(spectrum_name)
            data_file_name = data_dir_name+'/'+raw_name+'/'+raw_name+'.out'
            new_one_spectra_data = OneSpectrumActivationData()
            new_one_spectra_data.read_raw_file(data_file_name)
            self.activation_data[spectrum_name] = new_one_spectra_data
        # read 5 data files
        return True

    def read_raw_spectrum_file(self,raw_name,spectrum_name):
        data_dir_name = BasicPath.get_spectra_dir(spectrum_name)
        data_file_name = data_dir_name + '/' + raw_name +'/'+raw_name+'.out'
        new_one_spectra_data = OneSpectrumActivationData()
        new_one_spectra_data.read_raw_file(data_file_name)
        self.activation_data[spectrum_name] = new_one_spectra_data
        return True

    def get_spectra_data(self, spectrum_name):
        if spectrum_name in self.activation_data:
            return self.activation_data[spectrum_name]
        else:
            raise(YSPException("Cannot find data for spectrum: \"",spectrum_name,"\""))
            return None

    def __imul__(self, number):
        for key,data in self.activation_data.items():
            data *= number
        return self

    def __iadd__(self, other):
        assert (len(self.activation_data) == len(other.activation_data))
        for key, data in self.activation_data.items():
            if key in other.activation_data:
                data += other.activation_data[key]
        return self

class OneSpectrumActivationData(BaseData):
    def __init__(self):
        self.all_steps_activation_data = []
        self.path_way = MaterialPathWays()

    def read_raw_file(self, inputfilename):
        lines = []
        opensucessful = False
        with open(inputfilename) as inputfile:
            lines.extend(inputfile.readlines())
        opensucessful = True
        self.path_way.read_raw_lines(lines)
        startlinesforsteps = []
        for i in range(0, len(lines)):
            if lines[i].startswith('1* * * * * TIME INTERVAL'):
                startlinesforsteps.append(i)
        startlinesforsteps.append(len(lines))
        # if need to skip previous time steps, need to change the range
        for i in range(len(startlinesforsteps)-7, len(startlinesforsteps)):
            onestepdata = OneSpectrumOneStepActivationData()
            try:
                onestepdata.read_raw_lines(lines, startlinesforsteps[i - 1], startlinesforsteps[i])
            except Exception as err:
                print(err.args)
            self.all_steps_activation_data.append(onestepdata)
        return opensucessful

    def __imul__(self, number):
        for data in self.all_steps_activation_data:
            data *= number
        self.path_way *= number
        return self

    def __iadd__(self, other):
        if(len(self.all_steps_activation_data) != len(other.all_steps_activation_data)):
            print("here")
        for i in range(0,len(self.all_steps_activation_data)):
            self.all_steps_activation_data[i] += other.all_steps_activation_data[i]
        self.path_way += other.path_way
        return self

class OneSpectrumOneStepActivationData(BaseData):
    param_names = ['activity(Bq/kg)',
                   'activity_no_tritium(Bq/kg)',
                   'alpha_heat(kW/kg)',
                   'beta_heat(kW/kg)',
                   'gamma_heat(kW/kg)',
                   'total_heat(kW/kg)',
                   'total_heat_ex_tritium(kW/kg)',
                   'origin_mass(kg)',
                   'cur_mass(kg)',
                   'neutron_flux(n/cm**2/s)',
                   'number_fission',
                   'dose_rate(Sv/h)',
                   'ingestion_dose(Sv/kg)',
                   'inhalation_dose(Sv/kg)',
                   'ingestion_dose_ex_tritium(Sv/kg)',
                   'inhalation_dose_ex_tritium(Sv/kg)',
                   'gase_rate(appm/sec)']
    data_position = []

    def __init__(self):
        self.time = 0.0
        self.nuclides = dict()  # nuclides and their parameters
        self.parameters = dict()
        self.gamma_erg_bin = []
        self.gamma_spectra_cc = []
        self.gamma_spectra_power = []
        self.ok = False

    def read_raw_lines(self, lines, startidx, endidx):
        # nuclides info (first)
        nuclide_data_start_idx = startidx + 4
        nuclide_data_end_idx = nuclide_data_start_idx
        for i in range(nuclide_data_start_idx, endidx):
            if lines[i].startswith('0'):
                nuclide_data_end_idx = i
                break
        for i in range(nuclide_data_start_idx, nuclide_data_end_idx):
            one_nuclide_data = OneNuclideData()
            if one_nuclide_data.read_raw_line(lines[i]):
                self.nuclides[one_nuclide_data.nuclide_name] = one_nuclide_data
        # total info
        for i in range(4, 100):
            if lines[nuclide_data_end_idx+i].find('TOTAL ACTIVITY FOR')>0:
                self.parameters['activity(Bq/kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break

        #self.parameters['activity(Bq/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 5][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx+i].find('TOTAL ACTIVITY EXCLUDING TRITIUM')>0:
                self.parameters['activity_no_tritium(Bq/kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['activity_no_tritium(Bq/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 6][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx+i].find('TOTAL ALPHA HEAT PRODUCTION')>0:
                self.parameters['alpha_heat(kW/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 7][40:51])
                break
        #self.parameters['alpha_heat(kW/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 7][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx+i].find('TOTAL BETA  HEAT PRODUCTION')>0:
                self.parameters['beta_heat(kW/kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['beta_heat(kW/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 8][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('TOTAL GAMMA HEAT PRODUCTION') > 0:
                self.parameters['gamma_heat(kW/kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['gamma_heat(kW/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 9][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('TOTAL HEAT PRODUCTION') > 0:
                self.parameters['total_heat(kW/kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][90:101])
                break;
        #self.parameters['total_heat(kW/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 9][90:101])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('TOTAL HEAT EX TRITIUM') > 0:
                self.parameters['total_heat_ex_tritium(kW/kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][90:101])
                break
        #self.parameters['total_heat_ex_tritium(kW/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 10][90:101])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('INITIAL TOTAL MASS OF MATERIAL') > 0:
                self.parameters['origin_mass(kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['origin_mass(kg)'] = eval_str_number(lines[nuclide_data_end_idx + 10][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('TOTAL MASS OF MATERIAL') > 0:
                self.parameters['cur_mass(kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['cur_mass(kg)'] = eval_str_number(lines[nuclide_data_end_idx + 11][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('NEUTRON  FLUX DURING INTERVAL') > 0:
                self.parameters['neutron_flux(n/cm**2/s)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['neutron_flux(n/cm**2/s)'] = eval_str_number(lines[nuclide_data_end_idx + 12][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('NUMBER OF FISSIONS') > 0:
                self.parameters['number_fission'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['number_fission'] = eval_str_number(lines[nuclide_data_end_idx + 13][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('INGESTION  HAZARD FOR ALL MATERIALS') > 0:
                self.parameters['ingestion_dose(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['ingestion_dose(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 14][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('INHALATION HAZARD FOR ALL MATERIALS') > 0:
                self.parameters['inhalation_dose(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['inhalation_dose(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 15][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('INGESTION  HAZARD EXCLUDING TRITIUM') > 0:
                self.parameters['ingestion_dose_ex_tritium(Sv/h)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['ingestion_dose_ex_tritium(Sv/h)'] = eval_str_number(lines[nuclide_data_end_idx + 16][40:51])
        for i in range(4, 100):
            if lines[nuclide_data_end_idx + i].find('INHALATION HAZARD EXCLUDING TRITIUM') > 0:
                self.parameters['inhalation_dose_ex_tritium(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + i][40:51])
                break
        #self.parameters['inhalation_dose_ex_tritium(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 17][40:51])
        #self.parameters['inhalation_dose_ex_tritium(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 18][27:38])
        # spectra
        spectra_beg_idx = -1
        spectra_end_idx = -1
        for i in range(nuclide_data_end_idx + 20, endidx):
            if lines[i].find('GAMMA SPECTRUM AND ENERGIES/SECOND') > 0:
                spectra_beg_idx = i + 7
                break
        if spectra_beg_idx < 0:
            raise YSPException('cannot find spectra')
        for i in range(spectra_beg_idx, endidx):
            if lines[i].find('(') < 0:
                spectra_end_idx = i
                break
        if spectra_end_idx < 0:
            raise YSPException('spectra format error, no empty line after spectra')
        for i in range(spectra_beg_idx, spectra_end_idx):
            newline = lines[i]
            newline = lines[i][:63]+' '+lines[i][64:]
            (starterg, enderg, gamma_power, gammas) = num_pattern.findall(newline)
            self.gamma_erg_bin.append(eval(enderg))
            self.gamma_spectra_cc.append(eval(gamma_power))
            self.gamma_spectra_power.append(eval(gammas))
        # 'dose_rate(Sv/kg)'
        dose_rate_idx = -1
        for i in range(spectra_end_idx, endidx):
            if lines[i].find('DOSE RATE (PLANE SOURCE) FROM GAMMAS WITH ENERGY') > 0:
                dose_rate_idx = i
                break
        if dose_rate_idx < 0:
            self.parameters['dose_rate(Sv/h)'] = -1.0
        else:
            self.parameters['dose_rate(Sv/h)'] = eval_str_number(lines[dose_rate_idx][75:88])
        self.ok = True
        return True

    def __imul__(self, number):
        for key, val in self.nuclides.items():
            val *= number
        for key in self.parameters.keys():
            self.parameters[key] *= number
        assert(len(self.gamma_erg_bin) == len(self.gamma_spectra_cc) and len(self.gamma_spectra_cc) == len(self.gamma_spectra_power))
        for i in range(0, len(self.gamma_erg_bin)):
            self.gamma_spectra_cc[i] *= number
            self.gamma_spectra_power[i] *= number
        return self

    def __iadd__(self, other):
        for key, val in other.nuclides.items():
            if key in self.nuclides:
                self.nuclides[key] += other.nuclides[key]
            else:
                self.nuclides[key] = other.nuclides[key]
        for key, val in other.parameters.items():
            if key in self.parameters:
                self.parameters[key] += val
            else:
                self.parameters[key] = val
        assert(len(self.gamma_erg_bin) == len(other.gamma_erg_bin))
        for i in range(0,len(self.gamma_erg_bin)):
            self.gamma_spectra_cc[i] += other.gamma_spectra_cc[i]
            self.gamma_spectra_power[i] += other.gamma_spectra_power[i]
        return self


class OneNuclideData(BaseData):
    param_names = ['atoms',
                   'weight(g)',
                   'activity(Bq/kg)',
                   'beta_heat(kW/kg)',
                   'alpha_heat(kW/kg)',
                   'gamma_heat(kW/kg)',
                   'dose_rate(Sv/h)',
                   'ingestion_dose(Sv/kg)',
                   'inhalation_dose(Sv/kg)',
                   'Bq/A2_Ratio',
                   'half_life(sec)',
                   'total_heat(kW/kg)']

    def __init__(self):
        #  NUCLIDE ATOMS GRAMS Bq b-Energy a-Energy g-Energy DOSE RATE INGESTION INHALATION Bq/A2 HALF LIFE
        #                            kW       kW       kW      Sv/hr    DOSE(Sv/h)   DOSE(Sv/h) Ratio seconds
        self.params = {}
        self.nuclide_name = ''

    def read_raw_line(self, line):
        self.nuclide_name = line[0:9].replace(' ','')
        val_list = [a for a in line[14:].split(' ') if len(a) > 0
                    and a != '\n'
                    and ('#' not in a)
                    and ('<' not in a)
                    and ('?' not in a)]
        if len(val_list) < 11:
            return False
        for i in range(0, len(OneNuclideData.param_names) - 1):
            self.params[OneNuclideData.param_names[i]] = eval_str_number(val_list[i])
        if val_list[-1] == 'Stable':
            self.params['half_life(sec)'] = -1
        else:
            self.params['half_life(sec)'] = eval_str_number(val_list[-1])
        self.params['total_heat(kW/kg)'] = self.params['beta_heat(kW/kg)']+self.params['alpha_heat(kW/kg)']+self.params['gamma_heat(kW/kg)']
        return True

    def __imul__(self, number):
        for i in range(2, len(OneNuclideData.param_names) - 1):
            self.params[OneNuclideData.param_names[i - 2]] *= number
        self.params['total_heat(kW/kg)'] *= number
        return self

    def __iadd__(self, other):
        assert(self.nuclide_name == other.nuclide_name)
        for i in range(2, len(OneNuclideData.param_names) - 1):
            self.params[OneNuclideData.param_names[i - 2]] += other.params[OneNuclideData.param_names[i - 2]]
        self.params['total_heat(kW/kg)'] += other.params['total_heat(kW/kg)']
        return self


# ysp: we will need pickle for faster data persistence


def functest_activation():
    data_test = OneSpectrumActivationData()
    data_test.read_raw_file('C:/Users/ysp/Desktop/QT_practice/ITER DATA/Flux1/Fe/Fe.out')
    data_test *= 0.5
    data_test.path_way.output()
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    data_test2 = OneSpectrumActivationData()
    data_test2.read_raw_file('C:/Users/ysp/Desktop/QT_practice/ITER DATA/Flux1/Cu/Cu.out')
    data_test2 *= 0.5
    data_test2.path_way.output()
    data_test += data_test2
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    data_test.path_way.normalize()
    data_test.path_way.output()
    with open("C:/Users/ysp/Desktop/QT_practice/TestActivation.data", 'wb') as outdata:
        pickle.dump(data_test, outdata)
    for i in range(0,1000):
        with open("C:/Users/ysp/Desktop/QT_practice/TestActivation.data", 'rb') as indata:
            tmp = pickle.load(indata)
        print('over')
        if i % 100 == 0:
            print('it')


import timeit


if __name__ == '__main__':
    # for i in range(100):
    functest_activation()
    # print(timeit.timeit(stmt='functest()', setup='from __main__ import functest', number=1))
