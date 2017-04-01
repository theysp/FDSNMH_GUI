# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget,QDialog,QApplication, QHBoxLayout, QTableWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_WidgetParam import Ui_WidgetParam
from data_handling.material import MaterialListLibrary
from data_handling.material import Material

class QTableWidgetMaterial(QTableWidget):
    def __init__(self, material:Material=None, parent=None):
        super(QTableWidgetMaterial, self).__init__(parent)
        self.setColumnCount(2)
        self.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetMatComposition.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, item)
        self.horizontalHeader().setDefaultSectionSize(88)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setMinimumSectionSize(16)
        self.verticalHeader().setStretchLastSection(False)

    def retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        item = self.horizontalHeaderItem(0)
        item.setText(_translate("InputDlg", "Nuclide"))
        item = self.horizontalHeaderItem(1)
        item.setText(_translate("InputDlg", "Weight Proportion (%)"))

    def matInfoToUI(self, material):
        size = len(material.elements)

    def uiToMatInfo(self, material):
        return True
        return False