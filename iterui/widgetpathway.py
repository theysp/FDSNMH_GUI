# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget,QDialog,QApplication, QHBoxLayout, QTableWidgetItem, QFileDialog
from Ui_WidgetPathway import Ui_WidgetPathway
from data_handling.activationdata import *
from data_handling.material import Material


class WidgetPathway(QWidget, Ui_WidgetPathway):
    def __init__(self, data: OneSpectrumActivationData = None, parent=None):
        super(WidgetPathway, self).__init__(parent)
        self.setupUi(self)
        self.data = data
        self.material = Material()

    def data_to_ui(self, data: OneSpectrumActivationData, mat: Material):
        self.material = mat
        for i in range(0, self.tableWidgetPathway.rowCount()):
            for j in range(0, self.tableWidgetPathway.columnCount()):
                self.tableWidgetPathway.item(i, j).setText('')
        idx = 0
        search_keys = [a for a in self.plainTextEditSearchNuclide.toPlainText().split(' ')]
        self.data = data
        assert(self.data is not None)
        for nuclide, one_target_pathway in self.data.path_way.all_path_ways.items():
            all_keys_found = True
            for key in search_keys:
                if key not in nuclide:
                    all_keys_found = False
            if all_keys_found:
                one_target_pathway.normalize()
                for pathway in sorted(one_target_pathway.pathway.keys(), key=lambda a: -one_target_pathway.pathway[a]):
                    if one_target_pathway.pathway[pathway] < 1e-4:
                        continue
                    while idx >= self.tableWidgetPathway.rowCount():
                        self.tableWidgetPathway.insertRow(self.tableWidgetPathway.rowCount())
                        for i in range(0, self.tableWidgetPathway.columnCount()):
                            self.tableWidgetPathway.setItem(idx, i, QTableWidgetItem(''))
                    self.tableWidgetPathway.item(idx, 0).setText(nuclide)
                    self.tableWidgetPathway.item(idx, 1).setText("{0}".format(one_target_pathway.pathway[pathway]))
                    self.tableWidgetPathway.item(idx, 2).setText(pathway)
                    idx += 1
        self.tableWidgetPathway.scrollToTop()

    @pyqtSlot()
    def on_plainTextEditSearchNuclide_textChanged(self):
        self.data_to_ui(self.data)

    @pyqtSlot()
    def on_pushButtonSave_clicked(self):
        filename, _ = QFileDialog.getSaveFileName(parent=self, initialFilter='.txt')
        if filename:
            with open(filename, 'w') as fileout:
                fileout.write(self.material.name+" "+self.material.spectrum+'\n')
                fileout.write(self.material.to_string()+'\n')
                fileout.write('Target Nuclides\tPropotion\tPathway\n')
                search_keys = [a for a in self.plainTextEditSearchNuclide.toPlainText().split(' ')]
                for nuclide, one_target_pathway in self.data.path_way.all_path_ways.items():
                    all_keys_found = True
                    for key in search_keys:
                        if key not in nuclide:
                            all_keys_found = False
                    if all_keys_found:
                        one_target_pathway.normalize()
                        for pathway in sorted(one_target_pathway.pathway.keys(),
                                              key=lambda a: one_target_pathway.pathway[a]):
                            fileout.write("{}\t{:.2e}\t{}\n".format(nuclide,one_target_pathway.pathway[pathway],pathway))