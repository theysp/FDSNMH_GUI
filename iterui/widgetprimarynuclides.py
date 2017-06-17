# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget,QDialog,QApplication, QHBoxLayout
from Ui_WidgetPrimaryNuclides import Ui_WidgetPrimaryNuclides
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure, Axes
from data_handling.activationdata import *

class WidgetPrimaryNuclides(QWidget, Ui_WidgetPrimaryNuclides):
    cooling_times = ['1', '1.0e5', '1.0e6', '1.0e7', '1.0e8', '1.0e9', '1.5e9']
    param_names =  ['activity(Bq/kg)',
                   'total_heat(kW/kg)',
                   'dose_rate(Sv/h)',
                   'ingestion_dose(Sv/h)']
    show_names = ['Specific activity(Bq/kg)',
                  'Heat(kW/kg)',
                  'Dose rate(Sv/h)',
                  'Ingestion dose(Sv/h)']
    colors = ['#FA8072', '#7FFF00', '#87CEFA', '#8A2BE2', '#A9A9A9', '#E9967A', '#FF1493', '#9932CC', '#CD853F',
              '#FF7F50', '#2E8B57']

    def __init__(self, parent=None):
        super(WidgetPrimaryNuclides, self).__init__(parent)
        self.figure = None
        self.setupUi(self)
        self.axes = [None, None, None, None]
        self.checkButtons = [self.checkBoxAct, self.checkBoxHeat, self.checkBoxDose, self.checkBoxIng]
        for checkButton in self.checkButtons:
            checkButton.clicked.connect(self.on_click)
        for time in WidgetPrimaryNuclides.cooling_times:
            self.comboBoxCoolingTime.addItem(time)
        self.comboBoxCoolingTime.setCurrentIndex(2)
        self.initialize_canvas()

    def initialize_canvas(self):
        self.figure = Figure(figsize=(8, 6), dpi=100, tight_layout=True)
        self.figure.set_facecolor('#F5F5F5')
        self.figure.subplots_adjust(left=0.08, top=0.92, bottom=0.1)
        self.canvas = FigureCanvas(self.figure)
        self.verticalLayoutPlot.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.verticalLayoutToolbarAndOtherWidgets.addWidget(self.toolbar)

    def data_to_ui(self, act_data: OneSpectrumActivationData):
        self.act_data = act_data
        self.update()
        self.initialize_figs()

    def initialize_figs(self):
        self.update()
        self.canvas.figure.clf()
        checked_button_num = 0
        for i in range(0, 4):
            if self.checkButtons[i].isChecked():
                checked_button_num += 1
        if checked_button_num is 0:
            return
        idx = 1
        if checked_button_num % 2 is 0:
            totalnum = checked_button_num * 50 + 20
        elif checked_button_num == 3:
            totalnum = 220
        else:
            totalnum = checked_button_num * 100 + 10
        for i in range(0, 4):
            if self.checkButtons[i].isChecked():
                self.axes[i] = self.figure.add_subplot(totalnum + idx)
                self.draw_axe(i)
                idx += 1
        self.canvas.draw()

    def draw_axe(self, idx):
        assert(self.act_data is not None)
        cooling_time_idx = self.comboBoxCoolingTime.currentIndex()
        assert(cooling_time_idx < len(self.act_data.all_steps_activation_data))
        one_step_data = self.act_data.all_steps_activation_data[cooling_time_idx]
        # get primary nuclides for xxx
        parameter_name = WidgetPrimaryNuclides.param_names[idx]
        # total_val = 0.0 # one_step_data.parameters[parameter_name]
        total_val = one_step_data.parameters[parameter_name]
        if total_val <= 0.0:
            self.axes[idx].set_title("Primary nuclides for: "+parameter_name+" is not valid.\nBecause the total value is 0.")
            self.axes[idx].pie([],labels=[])
            return
        nuclides = []
        nuclide_props = []
        accumulate_amount = 0.0
        primary_limit = self.horizontalSliderPrimaryAmount.value()*1.0/100
        # for nuclide in one_step_data.nuclides.keys():
        #     total_val += one_step_data.nuclides[nuclide].params[parameter_name]
        for nuclide in sorted(one_step_data.nuclides.keys(), key=lambda a: -one_step_data.nuclides[a].params[parameter_name]):
            nuclides.append(nuclide)
            act_value = one_step_data.nuclides[nuclide].params[parameter_name]
            prop = act_value/total_val
            accumulate_amount += prop
            nuclide_props.append(prop)
            if accumulate_amount >= primary_limit:
                break
        if accumulate_amount > 0.999999:
            accumulate_amount = 1.0
        leftprop = 1-accumulate_amount
        if leftprop > 0.0001:
            nuclide_props.append(leftprop)
            nuclides.append('Other')
        self.axes[idx].pie(nuclide_props, labels=nuclides, colors=WidgetPrimaryNuclides.colors, autopct='%1.2f%%', shadow=True, startangle=90)
        show_name = WidgetPrimaryNuclides.show_names[idx]
        self.axes[idx].set_title("Primary nuclides for: "+show_name)
        self.axes[idx].axis('equal')
        return

    def on_click(self):
        self.update()
        self.initialize_figs()

    @pyqtSlot(int)
    def on_comboBoxCoolingTime_currentIndexChanged(self, idx):
        if self.figure is not None:
            self.initialize_figs()

    @pyqtSlot(int)
    def on_horizontalSliderPrimaryAmount_valueChanged(self, amount):
        self.labelPrimaryAmount.setText("{0}".format(amount))
        if self.figure is not None:
            self.initialize_figs()