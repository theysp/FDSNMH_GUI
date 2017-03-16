# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WidgetPrimaryNuclides.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetPrimaryNuclides(object):
    def setupUi(self, WidgetPrimaryNuclides):
        WidgetPrimaryNuclides.setObjectName("WidgetPrimaryNuclides")
        WidgetPrimaryNuclides.resize(565, 474)
        self.verticalLayout = QtWidgets.QVBoxLayout(WidgetPrimaryNuclides)
        self.verticalLayout.setObjectName("verticalLayout")
        self.framePlot = QtWidgets.QFrame(WidgetPrimaryNuclides)
        self.framePlot.setMinimumSize(QtCore.QSize(300, 300))
        self.framePlot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePlot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framePlot.setObjectName("framePlot")
        self.verticalLayout.addWidget(self.framePlot)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(544, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonSavePlot = QtWidgets.QPushButton(WidgetPrimaryNuclides)
        self.pushButtonSavePlot.setObjectName("pushButtonSavePlot")
        self.horizontalLayout.addWidget(self.pushButtonSavePlot)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(WidgetPrimaryNuclides)
        QtCore.QMetaObject.connectSlotsByName(WidgetPrimaryNuclides)

    def retranslateUi(self, WidgetPrimaryNuclides):
        _translate = QtCore.QCoreApplication.translate
        WidgetPrimaryNuclides.setWindowTitle(_translate("WidgetPrimaryNuclides", "Form"))
        self.pushButtonSavePlot.setText(_translate("WidgetPrimaryNuclides", "Save"))

