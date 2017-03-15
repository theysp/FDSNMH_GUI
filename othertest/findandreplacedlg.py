# -*- coding: utf-8 -*-

"""
Module implementing FindAndReplaceDlg.
"""

from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QApplication

from Ui_findandreplacedlg import Ui_FindAndReplaceDlg


class FindAndReplaceDlg(QDialog, Ui_FindAndReplaceDlg):
    """
    Class documentation goes here.
    """
    find = pyqtSignal(str,bool,bool,bool,bool,bool)
    replace = pyqtSignal(str,str,bool,bool,bool,bool,bool)     
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(FindAndReplaceDlg, self).__init__(parent)
        self.setupUi(self)
        self.moreFrame.hide()
        #self.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.updateUi()        

    @pyqtSlot(str)
    def on_findLineEdit_textEdited(self, text):
        """
        Slot documentation goes here.

        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        self.updateUi()

    @pyqtSlot()
    def on_findButton_clicked(self):
        self.find.emit(self.findLineEdit.text(),
                       self.caseCheckBox.isChecked(),
                       self.wholeCheckBox.isChecked(),
                       self.backwardsCheckBox.isChecked(),
                       self.regexCheckBox.isChecked(),
                       self.ignoreNotesCheckBox.isChecked())        


    @pyqtSlot()
    def on_replaceButton_clicked(self):
        self.replace.emit(self.findLineEdit.text(),
                          self.replaceLineEdit.text(),
                          self.caseCheckBox.isChecked(),
                          self.wholeCheckBox.isChecked(),
                          self.backwardsCheckBox.isChecked(),
                          self.regexCheckBox.isChecked(),
                          self.ignoreNotesCheckBox.isChecked())

    def updateUi(self):
        enable = self.findLineEdit.text()
        self.findButton.setEnabled(bool(enable))
        self.replaceButton.setEnabled(bool(enable))

if __name__ == "__main__":
    import sys

    def find(what, *args):
        print("Find {0} {1}".format(what, [x for x in args]))

    def replace(old, new, *args):
        print("Replace {0} with {1} {2}".format(
              old, new, [x for x in args]))

    app = QApplication(sys.argv)
    form = FindAndReplaceDlg()
    form.find.connect(find)
    form.replace.connect(replace)
    form.show()
    app.exec_()