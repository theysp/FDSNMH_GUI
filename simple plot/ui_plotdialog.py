# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotdialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PlotDialog(object):
    def setupUi(self, PlotDialog):
        PlotDialog.setObjectName("PlotDialog")
        PlotDialog.resize(603, 443)
        self.verticalLayout = QtWidgets.QVBoxLayout(PlotDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(PlotDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonPlot = QtWidgets.QPushButton(PlotDialog)
        self.buttonPlot.setObjectName("buttonPlot")
        self.horizontalLayout.addWidget(self.buttonPlot)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(PlotDialog)
        QtCore.QMetaObject.connectSlotsByName(PlotDialog)

    def retranslateUi(self, PlotDialog):
        _translate = QtCore.QCoreApplication.translate
        PlotDialog.setWindowTitle(_translate("PlotDialog", "Dialog"))
        self.buttonPlot.setText(_translate("PlotDialog", "PushButton"))

