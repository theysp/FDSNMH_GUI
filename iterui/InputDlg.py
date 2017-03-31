# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout
from Ui_InputDlg import Ui_InputDlg
from data_handling.material import MaterialListLibrary
from widgetparam import WidgetParam
import pickle
import os


class InputDlg(QDialog, Ui_InputDlg):
    def __init__(self, parent=None):
        super(InputDlg, self).__init__(parent)
        self.setupUi(self)
        self.matlib = MaterialListLibrary()
        self.init_ui_data()

    def init_ui_data(self):
        self.matlib.load_material_list()
        for mat in self.matlib.material_list:
            self.listWidgetMaterialLib.addItem(mat.name)

    @pyqtSlot(str)
    def on_textMaterialSearch_textChanged(self, text):
        if len(text) <= 0:
            for mat in self.matlib.material_list:
                self.listWidgetMaterialLib.addItem(mat.name)
            return
        self.listWidgetMaterialLib.clear()
        split_text = [a for a in text.split(' ') if len(a) > 0 and a != '\n']
        for mat in self.matlib.material_list:
            allin = True
            for word  in split_text:
                if not word in mat.name:
                    allin = False
                    break
            if allin:
                 self.listWidgetMaterialLib.addItem(mat.name)

    @pyqtSlot()
    def on_pushButtonSaveMaterialLib_clicked(self):
        self.matlib.save_material_list()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    resultDlg = InputDlg()
    resultDlg.show()
    sys.exit(app.exec_())