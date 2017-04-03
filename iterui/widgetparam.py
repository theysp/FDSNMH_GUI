# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget,QDialog,QApplication, QHBoxLayout
from Ui_WidgetParam import Ui_WidgetParam
from data_handling.activationdata import OneSpectrumActivationData


class WidgetParam(QWidget, Ui_WidgetParam):
    def __init__(self, parent=None):
        super(WidgetParam, self).__init__(parent)
        self.setupUi(self)

    def ui_to_data(self, act_data: OneSpectrumActivationData):
        for i in range(0,len(act_data.all_steps_activation_data)):
            one_step_data = act_data.all_steps_activation_data[i]
            item = self.tableWidgetParams.item(i, 0)
            item.setText(one_step_data.)