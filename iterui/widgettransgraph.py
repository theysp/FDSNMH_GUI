# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget,QDialog,QApplication, QHBoxLayout
from Ui_WidgetTransGraph import Ui_WidgetTransGraph
from data_handling.activationdata import OneSpectrumActivationData
from PyQt5.QtWidgets import QTableWidgetItem, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class WidgetTransGraph(QWidget, Ui_WidgetTransGraph):
    def __init__(self, parent=None):
        super(WidgetTransGraph, self).__init__(parent)
        self.setupUi(self)

    def value_nuclide(nuclide, act_data: OneSpectrumActivationData):
        # cooling times: ['1', '1.0e5', '1.0e6', '1.0e7', '1.0e8', '1.0e9', '1.5e9']
        order_step = [2,0,1,3,4,5,6]
        for i in range(0,7):
            if nuclide in act_data.all_steps_activation_data[i].nuclides:
                return act_data.all_steps_activation_data[i].nuclides[nuclide].params['activity(Bq)']
        return -1.0

    def data_to_ui(self, act_data: OneSpectrumActivationData):
        self.act_data = act_data
        self.nuclides_trans_data = {}
        self.ordered_nuclides = []
        all_nuclides_names = set()
        # get order
        for i in range(0, len(act_data.all_steps_activation_data)):
            one_step_data = act_data.all_steps_activation_data[i]
            for one_nuclide_data in one_step_data.nuclides.values():
                all_nuclides_names.add(one_nuclide_data.nuclide_name)
        for i in range(0, len(act_data.all_steps_activation_data)):
            one_step_data = act_data.all_steps_activation_data[i]
            for one_nuclide_data in one_step_data.nuclides.values():
                if one_nuclide_data.nuclide_name not in self.nuclides_trans_data:
                    self.nuclides_trans_data[one_nuclide_data.nuclide_name] = []
                self.nuclides_trans_data[one_nuclide_data.nuclide_name].append(one_nuclide_data.params['weight(g)'])
            for nuclide_name in all_nuclides_names:
                if nuclide_name not in one_step_data.nuclides:
                    if nuclide_name not in self.nuclides_trans_data:
                        self.nuclides_trans_data[nuclide_name] = []
                    self.nuclides_trans_data[nuclide_name].append(1e-50)
        self.ordered_nuclides = sorted(all_nuclides_names, key=lambda a: -WidgetTransGraph.value_nuclide(a, self.act_data))
        self.initialize_table_nuclides()
        self.initialize_canvas()
        self.initialize_figs()

    def initialize_table_nuclides(self):
        new_item1 = QTableWidgetItem()
        new_item2 = QTableWidgetItem()
        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(0, 0, new_item1)
        self.tableWidget.setItem(0, 1, new_item2)
        self.major_checkBox = QCheckBox(self)
        self.major_checkBox.setText('')
        self.tableWidget.setCellWidget(0, 0, self.major_checkBox)
        self.major_checkBox.setChecked(True)
        self.major_checkBox.clicked.connect(self.on_major_check)
        self.sub_checkBoxs = {}
        for i in range(1, len(self.ordered_nuclides)+1):
            while self.tableWidget.rowCount() <= i:
                self.tableWidget.insertRow(self.tableWidget.rowCount())
            new_item1 = QTableWidgetItem('')
            self.tableWidget.setItem(i, 0, new_item1)
            cur_nuclide_name = self.ordered_nuclides[i-1]
            self.sub_checkBoxs[cur_nuclide_name] = QCheckBox(self)
            self.sub_checkBoxs[cur_nuclide_name].setChecked(True)
            self.sub_checkBoxs[cur_nuclide_name].clicked.connect(self.on_sub_check)
            self.tableWidget.setCellWidget(i, 0, self.sub_checkBoxs[cur_nuclide_name])
            new_item2 = QTableWidgetItem(self.ordered_nuclides[i-1])
            self.tableWidget.setItem(i, 1, new_item2)

    def initialize_canvas(self):
        self.figure = Figure(figsize=(8, 6), dpi=100, tight_layout=True)
        self.figure.set_facecolor('#F5F5F5')
        self.figure.subplots_adjust(left=0.08, top=0.92, bottom=0.1)
        self.canvas = FigureCanvas(self.figure)

        self.verticalLayoutPlot.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas,self.framePlot)
        self.verticalLayoutPlot.addWidget(self.toolbar)

    def initialize_figs(self):
        cooling_times = ['1', '1.0e5', '1.0e6', '1.0e7', '1.0e8', '1.0e9', '1.5e9']
        self.figure.clf()
        self.axe = self.figure.add_subplot(111)
        self.axe.hold(True)
        self.axe.set_xscale('log')
        self.axe.set_yscale('log')
        self.axe.set_xlim([1, 2e9])
        self.axe.set_ylim([1e-40, 1000])
        for key, checkBox in self.sub_checkBoxs.items():
            if checkBox.isChecked():
                self.axe.plot(xs=[1, 1.0e5, 1.0e6, 1.0e7, 1.0e8, 1.0e9], ys=self.nuclides_trans_data[key], label=key)
        self.canvas.draw()

    def on_major_check(self):
        self.update()
        if self.major_checkBox.isChecked():
            for checkBox in self.sub_checkBoxs.values():
                checkBox.setChecked(True)
        else:
            for checkBox in self.sub_checkBoxs.values():
                checkBox.setChecked(False)
        self.initialize_figs()

    def on_sub_check(self):
        self.update()
        all_checked = True
        all_un_checked = True
        for key, val in self.sub_checkBoxs.items():
            if val.isChecked():
                all_un_checked = False
            else:
                all_checked = False
            if (not all_un_checked) and (not all_checked):
                break
        if all_checked:
            self.on_major_check.setChecked(True)
        if all_un_checked:
            self.on_major_check.setChecked(False)
        self.initialize_figs()