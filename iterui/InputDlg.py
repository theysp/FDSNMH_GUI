# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout, QListWidgetItem, QListWidget, QMessageBox
from Ui_InputDlg import Ui_InputDlg
from data_handling.material import MaterialListLibrary
from widgetparam import WidgetParam
from data_handling.material import *
from ShowResultDlg import ShowResultDlg
import pickle
import os
import copy
import sys
from PyQt5.QtGui import QIcon
import traceback

class InputDlg(QDialog, Ui_InputDlg):
    def __init__(self, parent=None):
        super(InputDlg, self).__init__(parent)
        self.setupUi(self)
        self.matlib = MaterialListLibrary()
        self.init_ui_data()
        self.resultdlgs = []
        self.tableWidgetMatComposition.init_mat_table()
        self.setWindowIcon(QIcon('fds.ico'))

    def init_ui_data(self):
        while self.listWidgetMaterialLib.count() > 0:
            item = self.listWidgetMaterialLib.takeItem(0)
        self.listWidgetMaterialLib.clear()
        self.matlib.load_material_list()
        text = self.textMaterialSearch.text()
        split_text = [a for a in text.split(' ') if len(a) > 0 and a != '\n']
        spectra_name_list = BasicPath.get_spectra_list()
        for spectrum_name in sorted(spectra_name_list):
            self.comboBoxSelectSpectra.addItem(spectrum_name)
        for mat_name in sorted(self.matlib.materials.keys(), key=lambda a: a):
            allin = True
            for word in split_text:
                if not (word in mat_name):
                    allin = False
                    break
            if allin:
                self.listWidgetMaterialLib.addItem(mat_name)

    def current_material(self):
        mat_ret = self.tableWidgetMatComposition.ui_to_mat_info()
        if mat_ret is None:
            return None
        else:
            mat_ret.name = self.textMatName.toPlainText()
            return mat_ret

    def show_message(self, msg):
        msg_box = QMessageBox()
        msg_box.setText(msg)
        msg_box.exec()

    @pyqtSlot()
    def on_listWidgetMaterialLib_itemSelectionChanged(self):
        selected_row_idx = self.listWidgetMaterialLib.currentRow()
        if selected_row_idx >= 0:
            mat_name = self.listWidgetMaterialLib.item(selected_row_idx).text()
            self.tableWidgetSelectedMatComposition.mat_info_to_ui(self.matlib.materials[mat_name])
        else:
            self.tableWidgetSelectedMatComposition.init_mat_table()

    @pyqtSlot(str)
    def on_textMaterialSearch_textChanged(self, text):
        if len(text) <= 0:
            keys = self.matlib.materials.keys()
            for matname in sorted(keys, key=lambda a: a):
                self.listWidgetMaterialLib.addItem(matname)
            return
        while self.listWidgetMaterialLib.count() > 0:
            item = self.listWidgetMaterialLib.takeItem(0)
        self.listWidgetMaterialLib.clear()
        split_text = [a for a in text.split(' ') if len(a) > 0 and a != '\n']
        for mat_name in sorted(self.matlib.materials.keys(), key=lambda a: a):
            allin = True
            for word in split_text:
                if not(word in mat_name):
                    allin = False
                    break
            if allin:
                 self.listWidgetMaterialLib.addItem(mat_name)

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
                    self.show_message('\"'+material.name + "\" already exists in the material library, please change the material name to save it.")
                    return
                except Exception:
                    pass
                self.init_ui_data()

    @pyqtSlot()
    def on_pushButtonUpdateMaterialLib_clicked(self):
        self.matlib.save_material_list()

    @pyqtSlot()
    def on_pushButtonDeleteMatFromLib_clicked(self):
        selected_item = self.listWidgetMaterialLib.currentItem()
        if selected_item:
            reply = QMessageBox.information(self, "Question", "Do you really want to delete "
            "the material \"{}\" from the meterial library?".format(selected_item.text()),
                                             QMessageBox.Ok |QMessageBox.Cancel)
            if reply == QMessageBox.Ok:
                self.matlib.del_material(selected_item.text())
                self.on_pushButtonUpdateMaterialLib_clicked()
                self.init_ui_data()
                self.matlib.save_material_list()

    @pyqtSlot()
    def on_pushButtonClearCurrentMat_clicked(self):
        self.tableWidgetMatComposition.init_mat_table()

    @pyqtSlot()
    def on_pushButtonShowResult_clicked(self):
        cur_mat = copy.deepcopy(self.tableWidgetSelectedMatComposition.cur_material) #self.current_material()
        if cur_mat is None:
            self.show_message('Please select the material needed to'
            ' be displayed from the material libraray')
            return
        #spectra_names = BasicPath.get_spectra_list()
        cur_spectrum_name = self.comboBoxSelectSpectra.currentText()
        try:
            self.setCursor(Qt.WaitCursor)
            #cur_mat_cache = cur_mat.get_cached_material()
            index = self.comboBoxSelectSpectra.currentIndex()
            cur_mat_cache = cur_mat.get_cached_spectrum_material(cur_spectrum_name)
            if cur_mat_cache is not None: # in case different material with the same name
                cur_mat.normalize()
                for elem in cur_mat.elements.keys():
                    if not(elem in cur_mat_cache.elements.keys()):
                        cur_mat_cache = None
                        break
                    elif abs(cur_mat.elements[elem] - cur_mat_cache.elements[elem]) > 1e-5:
                        cur_mat_cache = None
                        break
            if cur_mat_cache is None:
                if cur_mat.calculate_spectrum_activation(cur_spectrum_name):
                    print("calculate activation of material: "+cur_mat.name)
                    cur_mat_cache = cur_mat
                    cur_mat_cache.cache_spectrum_material(cur_spectrum_name)
            else:
                print("loaded cached material: " + cur_mat.name)
            #if cur_mat.calculate_activation():
            if cur_mat_cache is not None:
                self.resultdlgs.append(ShowResultDlg(cur_mat_cache))
                self.resultdlgs[-1].setWindowTitle('Activation data of material \"{0}\", spectrum \"{1}\"'
                                                   .format(cur_mat_cache.name, cur_spectrum_name))
                self.resultdlgs[-1].show()
            else:
                self.show_message('The activation data of \'{0}\' calculation failed.'.format(cur_mat.name))
            self.setCursor(Qt.ArrowCursor)
        except YSPException as error:
            self.show_message("Error in calculating activation properties for material: "
                    +cur_mat.name+" under spectrum: "+cur_spectrum_name+", info: "+error.message
                    +"\nPlease check if the files under " + BasicPath.getspectra_dir(cur_spectrum_name))
            traceback.print_exc()
            self.show_message("Error: "
        except Exception as err:
            self.show_message("Unknow error. Please check the console for more information.")
            print(err)
            traceback.print_exc()
        finally:
            self.setCursor(Qt.ArrowCursor)

if __name__ == "__main__":
    # try:
    app = QApplication(sys.argv)
    resultDlg = InputDlg()
    resultDlg.show()
    sys.exit(app.exec_())
   #  except Exception as err:
   #     print(err.args)