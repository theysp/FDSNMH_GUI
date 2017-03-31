# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QApplication, QHBoxLayout
from Ui_InputDlg import Ui_InputDlg
from widgetparam import WidgetParam
import pickle
import os


class MaterialListLibrary:
    material_list_file_name = "../Data Save/matlist.txt"
    def __init__(self):
        self.material_list = []
        self.load_material_list()

    def load_material_list(self):
        if os.path.exists(MaterialListLibrary.material_list_file_name):
            with open(MaterialListLibrary.material_list_file_name) as list_file:
                lines = list_file.readlines()
                for line in lines:
                    line = line.strip('\r\n\s')
                    if len(line) > 0:
                        self.material_list = line

    def save_material_list(self):
        with open(MaterialListLibrary.material_list_file_name, 'w') as list_file:
            for mat in self.material_list:
                list_file.write(mat)


class InputDlg(QDialog, Ui_InputDlg):
    def __init__(self, parent=None):
        super(InputDlg, self).__init__(parent)
        self.setupUi(self)
        self.init_ui_data()

    def init_ui_data(self):
        self.matlist = MaterialListLibrary()
        self.listViewMaterialLib