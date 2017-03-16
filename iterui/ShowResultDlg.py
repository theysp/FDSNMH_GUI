# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QApplication, QHBoxLayout
from Ui_ShowResultDlg import Ui_ShowResultDlg

class ShowResultDlg(QDialog, Ui_ShowResultDlg):
    def __init__(self, parent=None):
        super(ShowResultDlg, self).__init__(parent)
        self.setupUi(self)

