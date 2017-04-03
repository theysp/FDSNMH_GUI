# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QApplication, QHBoxLayout
from Ui_ShowResultDlg import Ui_ShowResultDlg
from widgetparam import WidgetParam
from data_handling.material import *


class ShowResultDlg(QDialog, Ui_ShowResultDlg):
    def __init__(self, material, spectraidx, parent=None):
        super(ShowResultDlg, self).__init__(parent)
        self.setupUi(self)
        self.material = material
        self.spectra_idx = spectraidx

    def data_to_uis(self):
        

