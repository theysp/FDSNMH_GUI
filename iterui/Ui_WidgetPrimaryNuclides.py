# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/WidgetPrimaryNuclides.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetPrimaryNuclides(object):
    def setupUi(self, WidgetPrimaryNuclides):
        WidgetPrimaryNuclides.setObjectName("WidgetPrimaryNuclides")
        WidgetPrimaryNuclides.resize(768, 474)
        self.verticalLayout = QtWidgets.QVBoxLayout(WidgetPrimaryNuclides)
        self.verticalLayout.setObjectName("verticalLayout")
        self.framePlot = QtWidgets.QFrame(WidgetPrimaryNuclides)
        self.framePlot.setMinimumSize(QtCore.QSize(300, 300))
        self.framePlot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePlot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framePlot.setObjectName("framePlot")
        self.verticalLayoutPlot = QtWidgets.QVBoxLayout(self.framePlot)
        self.verticalLayoutPlot.setObjectName("verticalLayoutPlot")
        self.verticalLayout.addWidget(self.framePlot)
        self.verticalLayoutToolbarAndOtherWidgets = QtWidgets.QVBoxLayout()
        self.verticalLayoutToolbarAndOtherWidgets.setObjectName("verticalLayoutToolbarAndOtherWidgets")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBoxAct = QtWidgets.QCheckBox(WidgetPrimaryNuclides)
        self.checkBoxAct.setChecked(True)
        self.checkBoxAct.setObjectName("checkBoxAct")
        self.horizontalLayout.addWidget(self.checkBoxAct)
        self.checkBoxDose = QtWidgets.QCheckBox(WidgetPrimaryNuclides)
        self.checkBoxDose.setChecked(True)
        self.checkBoxDose.setObjectName("checkBoxDose")
        self.horizontalLayout.addWidget(self.checkBoxDose)
        self.checkBoxHeat = QtWidgets.QCheckBox(WidgetPrimaryNuclides)
        self.checkBoxHeat.setChecked(True)
        self.checkBoxHeat.setObjectName("checkBoxHeat")
        self.horizontalLayout.addWidget(self.checkBoxHeat)
        self.checkBoxIng = QtWidgets.QCheckBox(WidgetPrimaryNuclides)
        self.checkBoxIng.setChecked(True)
        self.checkBoxIng.setObjectName("checkBoxIng")
        self.horizontalLayout.addWidget(self.checkBoxIng)
        self.label = QtWidgets.QLabel(WidgetPrimaryNuclides)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxCoolingTime = QtWidgets.QComboBox(WidgetPrimaryNuclides)
        self.comboBoxCoolingTime.setObjectName("comboBoxCoolingTime")
        self.horizontalLayout.addWidget(self.comboBoxCoolingTime)
        self.label_2 = QtWidgets.QLabel(WidgetPrimaryNuclides)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.labelPrimaryAmount = QtWidgets.QLabel(WidgetPrimaryNuclides)
        self.labelPrimaryAmount.setObjectName("labelPrimaryAmount")
        self.horizontalLayout.addWidget(self.labelPrimaryAmount)
        self.horizontalSliderPrimaryAmount = QtWidgets.QSlider(WidgetPrimaryNuclides)
        self.horizontalSliderPrimaryAmount.setMinimumSize(QtCore.QSize(100, 0))
        self.horizontalSliderPrimaryAmount.setMinimum(60)
        self.horizontalSliderPrimaryAmount.setMaximum(100)
        self.horizontalSliderPrimaryAmount.setSliderPosition(95)
        self.horizontalSliderPrimaryAmount.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderPrimaryAmount.setObjectName("horizontalSliderPrimaryAmount")
        self.horizontalLayout.addWidget(self.horizontalSliderPrimaryAmount)
        spacerItem = QtWidgets.QSpacerItem(544, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayoutToolbarAndOtherWidgets.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayoutToolbarAndOtherWidgets)

        self.retranslateUi(WidgetPrimaryNuclides)
        QtCore.QMetaObject.connectSlotsByName(WidgetPrimaryNuclides)

    def retranslateUi(self, WidgetPrimaryNuclides):
        _translate = QtCore.QCoreApplication.translate
        WidgetPrimaryNuclides.setWindowTitle(_translate("WidgetPrimaryNuclides", "Form"))
        self.checkBoxAct.setText(_translate("WidgetPrimaryNuclides", "Act"))
        self.checkBoxDose.setText(_translate("WidgetPrimaryNuclides", "Dose"))
        self.checkBoxHeat.setText(_translate("WidgetPrimaryNuclides", "Heat"))
        self.checkBoxIng.setText(_translate("WidgetPrimaryNuclides", "Ing"))
        self.label.setText(_translate("WidgetPrimaryNuclides", "Cooling time (s):"))
        self.label_2.setText(_translate("WidgetPrimaryNuclides", "Contribution threshold (%):"))
        self.labelPrimaryAmount.setText(_translate("WidgetPrimaryNuclides", "95"))

