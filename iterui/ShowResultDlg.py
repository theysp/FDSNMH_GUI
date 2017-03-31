# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QApplication, QHBoxLayout
from Ui_ShowResultDlg import Ui_ShowResultDlg
from widgetparam import WidgetParam

class ShowResultDlg(QDialog, Ui_ShowResultDlg):
    def __init__(self, parent=None):
        super(ShowResultDlg, self).__init__(parent)
        self.setupUi(self)


