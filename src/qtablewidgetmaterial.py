# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShowResult.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget,QDialog,QApplication, QHBoxLayout, QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QLineEdit, QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.Qt import QKeyEvent
from PyQt5.QtGui import QBrush, QColor
from Ui_WidgetParam import Ui_WidgetParam
from data_handling.material import *
from base.base import BasicPath


class QTableWidgetMaterial(QTableWidget):
    def __init__(self, editable=True, parent=None):
        super(QTableWidgetMaterial, self).__init__(parent)
        self.setColumnCount(2)
        self.setRowCount(1)
        item = QTableWidgetItem('')
        item.setBackground(QColor(200,200,200))
        self.setItem(0, 0, QTableWidgetItem(''))
        self.setItem(0, 1, QTableWidgetItem(''))
        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QColor(200, 200, 200))
        self.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, item)
        self.horizontalHeader().setDefaultSectionSize(88)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setMinimumSectionSize(16)
        self.verticalHeader().setStretchLastSection(False)
        self.retranslate_ui()
        self.cur_material = None
        self.elemlist = []
        self.elemlist.append('')
        with open(BasicPath.element_list_file_name) as input_elemnt:
            lines = [a for a in input_elemnt.readlines() if len(a) > 0]
            for line in lines:
                self.elemlist.append(line.strip('\r\n '))
        self.connect_signal_slots()
        self.editable = editable

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        item = self.horizontalHeaderItem(0)
        item.setText(_translate("InputDlg", "Element"))
        item = self.horizontalHeaderItem(1)
        item.setText(_translate("InputDlg", "Weight Proportion (%)"))

    def connect_signal_slots(self):
        self.currentCellChanged.connect(self.on_self_currentCellChanged)
        self.itemChanged.connect(self.on_self_itemChanged)

    def disconnect_signal_slots(self):
        self.currentCellChanged.disconnect()
        self.itemChanged.disconnect()

    def init_mat_table(self):
        self.cur_material = Material('')
        self.mat_info_to_ui(self.cur_material)

    def mat_info_to_ui(self, material:Material):
        self.cur_material = material
        self.disconnect_signal_slots()
        self.cur_material = material
        self.setRowCount(0)
        size = len(material.elements)
        if size > 0:
            self.setRowCount(size+1)
            row_idx = 0
            for key, val in material.elements.items():
                self.setItem(row_idx, 0, QTableWidgetItem(key))
                self.setItem(row_idx, 1, QTableWidgetItem('{0}'.format(val)))
                row_idx += 1
        else:
            size = 0
            self.setRowCount(1)
        self.setItem(size, 0, QTableWidgetItem(''))
        self.setItem(size, 1, QTableWidgetItem(''))
        self.connect_signal_slots()

    def ui_to_mat_info(self):
        if self.cur_material is None:
            return None
        material = Material()
        material.name = self.cur_material.name
        for i in range(0, self.rowCount()-1):
            if not self.item(i, 0).text() in self.elemlist:
                self.setCurrentCell(i,0)
                msg_box = QMessageBox()
                msg_box.setText('Error element name: \"'+self.item(i, 0).text()+'\"')
                msg_box.exec()
                return None
            isnumber = False
            try:
                number = eval(self.item(i, 1).text())
                isnumber = True
            except ValueError:
                isnumber = False
            if not isnumber:
                self.setCurrentCell(i,1)
                msg_box = QMessageBox()
                msg_box.setText('Error element propotion: \"' + self.item(i, 0).text() + '\"')
                msg_box.exec()
                return None
            material.add_element(self.item(i, 0).text(),eval(self.item(i, 1).text()))
        material.normalize()
        return material

    def on_self_currentCellChanged(self, p_int, p_int_1, p_int_2, p_int_3):
        # recover the previous cell to plaintext
        if p_int_3 == 0:
            old_combo = self.cellWidget(p_int_2, p_int_3)
            item = self.item(p_int_2, p_int_3)
            item.setText(old_combo.currentText())
            self.setCellWidget(p_int_2, p_int_3, None)
        # set widget to QComboBox with elements if select new item
        if p_int_1 == 0:
            item = self.item(p_int, p_int_1)
            elem_text = item.text()
            new_combo = QComboBox()
            new_combo = QComboBox()
            for elem in self.elemlist:
                new_combo.addItem(elem)
            if elem_text in self.elemlist[1:]:
                new_combo.setCurrentText(elem_text)
            else:
                new_combo.setCurrentText(self.elemlist[0])
            self.setCellWidget(p_int, p_int_1, new_combo)

    # if the last row has been updated, add new line to the table, means a new element
    def on_self_itemChanged(self, item):
        self.disconnect_signal_slots()
        irow = item.row()
        if irow == self.rowCount()-1:
            self.insertRow(self.rowCount())
            self.setItem(irow+1, 0, QTableWidgetItem(''))
            self.setItem(irow+1, 1, QTableWidgetItem(''))
        self.connect_signal_slots()

    # inherit the handler for pressing keys
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Delete:
            item = self.currentItem()
            row_idx = item.row()
            if row_idx < self.rowCount()-1:
                self.takeItem(row_idx, 0)
                self.takeItem(row_idx, 1)
                self.removeRow(row_idx)
        else:
            super(QTableWidgetMaterial,self).keyPressEvent(event)