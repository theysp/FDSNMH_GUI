# -*- coding: utf-8 -*-


class BasicPath:
    activation_data_path = '../ITER DATA'
    material_list_file_name = "../Data Save/matlist.txt"
    element_list_file_name = "../Data Save/elemlist.txt"


class YSPException(Exception):
    def __init__(self,*args):
        super(YSPException,self).__init__(self)


class MaterialAlreadyException(Exception):
    def __init__(self,*args):
        super(MaterialAlreadyException,self).__init__(self, args)