# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout, QListWidgetItem, QListWidget, QMessageBox
from Ui_InputDlg import Ui_InputDlg
from data_handling.material import MaterialListLibrary
from widgetparam import WidgetParam
from base.base import MaterialAlreadyException
from data_handling.material import *
import pickle
import os
import copy


class InputDlg(QDialog, Ui_InputDlg):
    def __init__(self, parent=None):
        super(InputDlg, self).__init__(parent)
        self.setupUi(self)
        self.matlib = MaterialListLibrary()
        self.init_ui_data()

    def init_ui_data(self):
        self.listWidgetMaterialLib.clear()
        self.matlib.load_material_list()
        keys = self.matlib.materials.keys()
        for matname in sorted(keys, key=lambda a: a):
            self.listWidgetMaterialLib.addItem(matname)

    def data_to_table(self, material, tableWidget: QtWidgets.QTableWidget):
        tableWidget.clear()
        tableWidget.insertRow(len(material.elements))
        for m in material.elements:
            tableWidget.item()

    @pyqtSlot()
    def on_listWidgetMaterialLib_itemSelectionChanged(self):
        selected_row_idx = self.listWidgetMaterialLib.currentRow()
        if selected_row_idx >= 0:
            mat_name = self.listWidgetMaterialLib.item(selected_row_idx).text()
            self.tableWidgetSelectedMatComposition.mat_info_to_ui(self.matlib.materials[mat_name])
        else:
            self.tableWidgetSelectedMatComposition.clear()

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
            for word in split_text:
                if not(word in mat.name):
                    allin = False
                    break
            if allin:
                 self.listWidgetMaterialLib.addItem(mat.name)

    @pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        if self.tableWidgetSelectedMatComposition.cur_material:
            new_mat = copy.deepcopy(self.tableWidgetSelectedMatComposition.cur_material)
            self.tableWidgetMatComposition.mat_info_to_ui(new_mat)
            self.textMatName.setPlainText(new_mat.name)

    @pyqtSlot()
    def on_pushButtonSave_clicked(self):
        if self.tableWidgetMatComposition.cur_material:
            material = self.tableWidgetMatComposition.ui_to_mat_info()
            material.name = self.textMatName.toPlainText()
            if material:
                try:
                    self.matlib.add_material(material)
                except MaterialAlreadyException as err:
                    msg_box = QMessageBox()
                    msg_box.setText('\"'+material.name + "\" already exists in the material library, please change the material name to save it.")
                    msg_box.exec()
                    return
                except Exception:
                    pass
                self.init_ui_data()

    @pyqtSlot()
    def on_pushButtonSaveMaterialLib_clicked(self):
        self.matlib.save_material_list()

import sys

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        resultDlg = InputDlg()
        resultDlg.show()
        sys.exit(app.exec_())
    except Exception as err:
        print(err.args)