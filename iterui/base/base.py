# -*- coding: utf-8 -*-


class YSPException(Exception):
    def __init__(self,*args):
        super(YSPException,self).__init__(self)
        self.message = ""
        for arg in args:
            self.message += "{}".format(arg)


class BasicPath:
    activation_data_path = '../ITER DATA'
    material_list_file_name = "../Data Save/matlist.txt"
    element_list_file_name = "../Data Save/elemlist.txt"
    element_cache_folder = "../Data Save/Cache"
    spectra_list_file_name = "../Data Save/spectralist.txt"
    inited_spectra_list = False
    spectra_dict = {}

    @staticmethod
    def init_spectra_dirs():
        if not BasicPath.inited_spectra_list:
            BasicPath.spectra_dict = {}
            with open(BasicPath.spectra_list_file_name) as spectra_list:
                for line in spectra_list:
                    if line.find('|') < 0:
                        next
                    line = line.strip('\r\n')
                    tmp_spect_name, tmp_dir_name = [a for a in line.split('|') if a != '']
                    tmp_spect_name = tmp_spect_name.strip(' ')
                    tmp_dir_name = tmp_dir_name.strip(' ')
                    if tmp_spect_name is None:
                        raise (YSPException('Empty spectrum name in file: ',BasicPath.spectra_list_file_name))
                    BasicPath.spectra_dict[tmp_spect_name] = tmp_dir_name
            BasicPath.inited_spectra_list = True

    @staticmethod
    def get_spectra_dir(spect_name):
        BasicPath.init_spectra_dirs()
        if spect_name in BasicPath.spectra_dict:
            return BasicPath.activation_data_path + '/'+BasicPath.spectra_dict[spect_name]
        raise (YSPException("Cannot find the directory name for spectrum: ",spect_name))

    @staticmethod
    def get_spectra_list():
        BasicPath.init_spectra_dirs()
        return BasicPath.spectra_dict.keys()

    def __init__(self, *args):
        pass