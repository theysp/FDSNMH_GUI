# -*- coding: utf-8 -*-


import numpy as np
import re
import copy

from pathway import PathWay

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


class ActivationData:
    def __init__(self):
        # 6 activity, dose rate, heat, ingestion dose, #6 spectrums
        self.activition_data = []

    def __init__(self, fispact_output):
        self.read_raw_file(fispact_output)

    def read_raw_file(self, matname):
        # obtain 5 files
        data_file_names = ['Flux1\\{0}\\{0}.out'.format(matname),
                           'Flux2\\{0}\\{0}.out'.format(matname),
                           'Flux4\\{0}\\{0}.out'.format(matname),
                           'Flux5\\{0}\\{0}.out'.format(matname),
                           'Flux6\\{0}\\{0}.out'.format(matname)]
        for file_name in data_file_names:
            new_one_spectra_data = OneSpectrumActivationData()
            new_one_spectra_data.read_raw_file(file_name)
            self.activition_data.append(new_one_spectra_data)
        # read 5 data files
        return False

    def get_spectra_data(self, spectraidx):
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
            # if need to skip previous time steps, need to change the range
            for i in range(len(startlinesforsteps)-6, len(startlinesforsteps)):
                onestepdata = OneSpectrumOneStepActivationData()
                try:
                    onestepdata.load_from_raw_lines(lines, startlinesforsteps[i - 1], startlinesforsteps[i])
                except Exception as err:
                    print(err.args)
                self.allStepsActivationData.append(onestepdata)
        finally:
            return opensucessful


class OneSpectrumOneStepActivationData:
    param_names = ['total_activity(Bq)',
                   'total_activity_no_tritium(Bq)',
                   'alpha_heat(kW)',
                   'beta_heat(kW)',
                   'gamma_heat(kW)',
                   'total_heat(kW)',
                   'total_heat_ex_tritium(kW)',
                   'origin_mass(kg)',
                   'cur_mass(kg)',
                   'neutron_flux(n/cm**2/s)',
                   'number_fission',
                   'dose_rate(Sv/kg)',
                   'ingestion_dose(Sv/kg)',
                   'inhalation_dose(Sv/kg)',
                   'ingestion_dose_ex_tritium(Sv/kg)',
                   'inhalation_dose_ex_tritium(Sv/kg)',
                   'gase_rate(appm/sec)']

    def __init__(self):
        self.time = 0.0
        self.nuclides = dict()  # 核素以及原子数比
        self.parameters = {}
        self.gamma_erg_bin = []
        self.gamma_spectra_cc = []
        self.gamma_spectra_power = []
        self.ok = False

    def load_from_raw_lines(self, lines, startidx, endidx):
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
        self.parameters['total_activity(Bq)'] = eval_str_number(lines[nuclide_data_end_idx + 5][40:51])
        self.parameters['total_activity_no_tritium(Bq)'] = eval_str_number(lines[nuclide_data_end_idx + 6][40:51])
        self.parameters['alpha_heat(kW)'] = eval_str_number(lines[nuclide_data_end_idx + 7][40:51])
        self.parameters['beta_heat(kW)'] = eval_str_number(lines[nuclide_data_end_idx + 8][40:51])
        self.parameters['gamma_heat(kW)'] = eval_str_number(lines[nuclide_data_end_idx + 9][40:51])
        self.parameters['total_heat(kW)'] = eval_str_number(lines[nuclide_data_end_idx + 9][90:101])
        self.parameters['total_heat_ex_tritium(kW)'] = eval_str_number(lines[nuclide_data_end_idx + 10][90:101])
        self.parameters['origin_mass(kg)'] = eval_str_number(lines[nuclide_data_end_idx + 10][40:51])
        self.parameters['cur_mass(kg)'] = eval_str_number(lines[nuclide_data_end_idx + 11][40:51])
        self.parameters['neutron_flux(n/cm**2/s)'] = eval_str_number(lines[nuclide_data_end_idx + 12][40:51])
        self.parameters['number_fission'] = eval_str_number(lines[nuclide_data_end_idx + 13][40:51])
        self.parameters['ingestion_dose(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 14][40:51])
        self.parameters['inhalation_dose(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 15][40:51])
        self.parameters['ingestion_dose_ex_tritium(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 16][40:51])
        self.parameters['inhalation_dose_ex_tritium(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 17][40:51])
        self.parameters['inhalation_dose_ex_tritium(Sv/kg)'] = eval_str_number(lines[nuclide_data_end_idx + 18][27:38])
        # spectra
        spectra_beg_idx = -1
        spectra_end_idx = -1
        for i in range(nuclide_data_end_idx + 20, endidx):
            if lines[i].find('GAMMA SPECTRUM AND ENERGIES/SECOND') > 0:
                spectra_beg_idx = i + 7
                break
        if spectra_beg_idx < 0:
            raise Exception('cannot find spectra')
        for i in range(spectra_beg_idx, endidx):
            if lines[i].find('(') < 0:
                spectra_end_idx = i
                break
        if spectra_end_idx < 0:
            raise Exception('spectra format error, no empty line after spectra')
        for i in range(spectra_beg_idx, spectra_end_idx):
            newline = lines[i]
            newline = lines[i][:63]+' '+lines[i][64:]
            (starterg, enderg, gamma_power, gammas) = num_pattern.findall(newline)
            self.gamma_erg_bin.append(enderg)
            self.gamma_spectra_cc.append(gamma_power)
            self.gamma_spectra_power.append(gammas)
        # 'dose_rate(Sv/kg)'
        dose_rate_idx = -1
        for i in range(spectra_end_idx, endidx):
            if lines[i].find('DOSE RATE (PLANE SOURCE) FROM GAMMAS WITH ENERGY') > 0:
                dose_rate_idx = i
                break
        if dose_rate_idx < 0:
            self.parameters['dose_rate(Sv/kg)'] = -1.0
        else:
            self.parameters['dose_rate(Sv/kg)'] = eval_str_number(lines[dose_rate_idx][75:88])
        self.ok = True
        return True


class OneNuclideData:
    param_names = ['atoms',
                   'weight(g)',
                   'activation(Bq)',
                   'beta_heat(kW)',
                   'alpha_heat(kW)',
                   'gamma_heat(kW)',
                   'dose_rate(Sv)',
                   'ingestion_dose(Sv)',
                   'inhalation_dose(Sv)',
                   'Bq/A2_Ratio',
                   'half_life(sec)']

    def __init__(self):
        #  NUCLIDE ATOMS GRAMS Bq b-Energy a-Energy g-Energy DOSE RATE INGESTION INHALATION Bq/A2 HALF LIFE
        #                            kW       kW       kW      Sv/hr    DOSE(Sv)   DOSE(Sv) Ratio seconds
        self.params = {}
        self.nuclide_name = ''

    def read_raw_line(self, line):
        val_list = [a for a in line.split(' ') if len(a) > 0 and a != '\n']
        if len(val_list) == 14:
            del val_list[2]
        if len(val_list) < 13:
            return False
        self.nuclide_name = val_list[0] + val_list[1]
        for i in range(2, len(OneNuclideData.param_names) - 1):
            self.params[OneNuclideData.param_names[i - 2]] = eval_str_number(val_list[i])
        if val_list[-1] == 'Stable':
            self.params['half_life(sec)'] = -1
        else:
            self.params['half_life(sec)'] = eval_str_number(val_list[-1])
        return True



def functest():
    data_test = OneSpectrumActivationData()
    data_test.read_raw_file('e:/tmp/Fe/Fe.out')
    print('finish')

import timeit

if __name__ == '__main__':
   # for i in range(100):
   #     functest(x)
    print(timeit.timeit(stmt='functest()', setup='from __main__ import functest',number=1))
