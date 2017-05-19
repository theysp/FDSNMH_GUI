# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import pyqtSlot,pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget,QDialog,QApplication, QHBoxLayout, QVBoxLayout, QFileDialog
from Ui_WidgetParam import Ui_WidgetParam
from PyQt5.Qt import QResizeEvent, QSize
from data_handling.activationdata import OneSpectrumActivationData
from PyQt5.QtWidgets import QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import os

class WidgetParam(QWidget, Ui_WidgetParam):
    param_names = ['activity(Bq/kg)',
                   'total_heat(kW/kg)',
                   'dose_rate(Sv/h)',
                   'ingestion_dose(Sv/h)']
    show_names = ['Specific activity(Bq/kg)',
                   'Heat(kW/kg)',
                   'Dose rate(Sv/h)',
                   'Ingestion dose(Sv/h)']
    cooling_times = [1, 1.0e5, 1.0e6, 1.0e7, 1.0e8, 1.0e9, 1.5e9]

    def __init__(self, parent=None):
        super(WidgetParam, self).__init__(parent)
        self.setupUi(self)
        self.act_data = None
        self.valuess = []   #valuess contains 4 values of the activation values
        self.initialize_canvas_parameters()
        self.axes = [None, None, None, None]
        self.checkButtons = [self.checkBoxAct, self.checkBoxHeat, self.checkBoxDose, self.checkBoxIng]
        self.extra_valuesss = {} #every extra valuess contains valuess for other element/material
        for checkButton in self.checkButtons:
            checkButton.clicked.connect(self.on_click)


    def data_to_ui(self, act_data: OneSpectrumActivationData):
        # show parameters of 6 cooling times
        self.act_data = act_data
        for idx in range(0,4):
            values = []
            for i in range(0, len(self.act_data.all_steps_activation_data)):
                one_step_data = self.act_data.all_steps_activation_data[i]
                values.append(one_step_data.parameters[WidgetParam.param_names[idx]])
            self.valuess.append(values)
        for i in range(0, len(self.valuess)):
            values = self.valuess[i]
            for j in range(0, len(values)):
                val = values[j]
                new_item = QTableWidgetItem('{0:.2e}'.format(val))
                self.tableWidgetParams.setItem(j, i+1, new_item)
        # plot data to plot widge
        self.initialize_figs_parameters()

    def initialize_canvas_parameters(self):
        # self.figure = Figure(figsize=(frame_size.width(), frame_size.height()), dpi=1, tight_layout=True)
        # #self.figure = Figure(figsize=(8, 6), dpi=100, tight_layout=True)
        # self.figure.set_facecolor('#F5F5F5')
        # self.figure.subplots_adjust(left=0.08, top=0.92, bottom=0.08)
        # # self.figure.subplots_adjust(left=3, top=3, bottom=3)
        # self.canvas = FigureCanvas(self.figure)
        # layout = QVBoxLayout(self.framePlot)
        # layout.setContentsMargins(0, 0, 0, 0)
        # layout.addWidget(self.canvas)
        # self.toolbar = NavigationToolbar(self.canvas, self.framePlot)
        # self.horizontalLayoutBelowPlot.addWidget(self.toolbar)
        # self.figure = Figure(figsize=(8, 6), dpi=100, tight_layout=True)
        frame_size = self.framePlot.size()
        self.figure = Figure(figsize=(frame_size.width()/100, frame_size.height()/100), dpi=100, tight_layout=True)
        self.figure.set_facecolor('#F5F5F5')
        self.figure.subplots_adjust(left=0.08, top=0.92, bottom=0.1)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self.framePlot)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas,self.framePlot)
        self.horizontalLayoutBelowPlot.addWidget(self.toolbar)

    def initialize_figs_parameters(self):
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

    def on_click(self):
        self.update()
        self.initialize_figs_parameters()

    def resizeEvent(self, event: QResizeEvent):
        super(WidgetParam, self).resizeEvent(event)
        new_size = event.size()
        new_width = new_size.width()
        one_column_width = new_width/6
        for i in range(1,4):
            if self.tableWidgetParams.columnWidth(i) < one_column_width:
                self.tableWidgetParams.setColumnWidth(i,one_column_width)

    def draw_axe(self, idx):
        assert(self.checkButtons[idx].isChecked())
        color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                          '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                          '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                          '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
#        values = []
#        for i in range(0, len(self.act_data.all_steps_activation_data)):
#            one_step_data = self.act_data.all_steps_activation_data[i]
#            values.append(one_step_data.parameters[WidgetParam.param_names[idx]])
        values = self.valuess[idx]

        assert(self.axes[idx] is not None)
        cur_axe = self.axes[idx]
        if values[0] < 1e-50:
            cur_axe.set_title(WidgetParam.show_names[idx]+" is all 0.")
            cur_axe.pie([], labels=[])
            return
        Font = {'family': 'Tahoma',
                'weight': 'bold', 'size': 10}
        # Abscissa
        cur_axe.set_xlim([1, 2e9])
        cur_axe.set_xticks(WidgetParam.cooling_times)
        cur_axe.set_xticklabels(WidgetParam.cooling_times, fontdict=Font)
        cur_axe.set_xlabel("Cooling time (s)", fontdict=Font)
        minval = min(values)+1e-20
        maxval = max(values)*1.5
        if len(self.extra_valuesss.items())>0:
            for val in self.extra_valuesss.values():
                minval = min(minval,min(val[idx])+1e-20)
                maxval = max(maxval,max(val[idx])*1.5)
        cur_axe.set_ylim([minval, maxval])
        # Ordinate
        cur_axe.set_ylabel(WidgetParam.show_names[idx], fontdict=Font)
        cur_axe.grid(True)  # Grid On
        if len(self.extra_valuesss.items()) == 0:
            cur_axe.plot(WidgetParam.cooling_times, values)
        else:
            color_idx = 0
            cur_axe.plot(WidgetParam.cooling_times, values, color=color_sequence[color_idx], label='current material')
            color_idx += 1
            for key, val in self.extra_valuesss.items():
                cur_axe.plot(WidgetParam.cooling_times, val[idx], color=color_sequence[color_idx], label=key)
                color_idx += 1
            cur_axe.legend()
        cur_axe.set_xscale('log')
        cur_axe.set_yscale('log')

    @pyqtSlot()
    def on_pushButtonSaveParam_clicked(self):
        filename, _ = QFileDialog.getSaveFileName(parent=self, initialFilter='.txt')
        if filename:
            with open(filename,'w') as fileout:
                fileout.write('cooling time\t ')
                for coolingtime in WidgetParam.cooling_times:
                    fileout.write('{0:.2e}'.format(coolingtime)+'\t')
                fileout.write('\n')
                for idx in range(0,len(self.valuess)):
                    values = self.valuess[idx]
                    name = WidgetParam.param_names[idx]
                    fileout.write(name+'\t')
                    for val in values:
                        fileout.write('{0:.2e}'.format(val)+'\t')
                    fileout.write('\n')

    @pyqtSlot()
    def on_pushButtonClear_clicked(self):
        self.setCursor(Qt.WaitCursor)
        self.extra_valuesss.clear()
        self.initialize_figs_parameters()
        self.setCursor(Qt.ArrowCursor)

    @pyqtSlot()
    def on_pushButtonLoadOther_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self)
        self.setCursor(Qt.WaitCursor)
        try:
            if filename:
                with open(filename, 'r') as filein:
                    lines = filein.readlines()
                    if len(lines)<5:
                        return
                    valss = []
                    for i in range(1, 5):
                        line = lines[i]
                        line = line.strip("\r\n")
                        val_strs = [a for a in line.split('\t') if len(a) > 0]
                        vals = []
                        for j in range(1,len(val_strs)):
                            vals.append(eval(val_strs[j]))
                        valss.append(vals)
                    self.extra_valuesss[os.path.basename(filename)] = valss
                self.initialize_figs_parameters()
        except Exception:
            pass
        self.setCursor(Qt.ArrowCursor)

