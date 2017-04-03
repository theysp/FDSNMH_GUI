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
from PyQt5.QtWidgets import QTableWidgetItem

class WidgetParam(QWidget, Ui_WidgetParam):
    def __init__(self, parent=None):
        super(WidgetParam, self).__init__(parent)
        self.setupUi(self)
        self.act_data = None

    def ui_to_data(self, act_data: OneSpectrumActivationData):
        # show parameters of 6 cooling times
        self.act_data = act_data
        for i in range(0, len(act_data.all_steps_activation_data)):
            one_step_data = act_data.all_steps_activation_data[i]
            param_names = ['total_activity(Bq)',
                           'total_heat(kW)',
                           'dose_rate(Sv/kg)',
                           'ingestion_dose(Sv/kg)']
            for j in range(0, 4):
                val = act_data.all_steps_activation_data[i].parameters[param_names[j]]
                new_item = QTableWidgetItem('{0}'.format(val))
                self.tableWidgetParams.setItem(i,j+1,new_item)
        # plot data to plot widget