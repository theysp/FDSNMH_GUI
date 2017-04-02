# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ShowResultDlg.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ShowResultDlg(object):
    def setupUi(self, ShowResultDlg):
        ShowResultDlg.setObjectName("ShowResultDlg")
        ShowResultDlg.resize(652, 484)
        self.verticalLayout = QtWidgets.QVBoxLayout(ShowResultDlg)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(ShowResultDlg)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxDecayPeriod = QtWidgets.QComboBox(ShowResultDlg)
        self.comboBoxDecayPeriod.setEditable(True)
        self.comboBoxDecayPeriod.setObjectName("comboBoxDecayPeriod")
        self.comboBoxDecayPeriod.addItem("")
        self.comboBoxDecayPeriod.addItem("")
        self.comboBoxDecayPeriod.addItem("")
        self.comboBoxDecayPeriod.addItem("")
        self.comboBoxDecayPeriod.addItem("")
        self.horizontalLayout.addWidget(self.comboBoxDecayPeriod)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidgetParameters = QtWidgets.QTabWidget(ShowResultDlg)
        self.tabWidgetParameters.setObjectName("tabWidgetParameters")
        self.Parameters = WidgetParam()
        self.Parameters.setObjectName("Parameters")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Parameters)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidgetParameters.addTab(self.Parameters, "")
        self.TransmutationGraph = WidgetTransGraph()
        self.TransmutationGraph.setObjectName("TransmutationGraph")
        self.tabWidgetParameters.addTab(self.TransmutationGraph, "")
        self.PrimaryNuclides = WidgetPrimaryNuclides()
        self.PrimaryNuclides.setObjectName("PrimaryNuclides")
        self.tabWidgetParameters.addTab(self.PrimaryNuclides, "")
        self.PathwayAnalysis = WidgetPathway()
        self.PathwayAnalysis.setObjectName("PathwayAnalysis")
        self.tabWidgetParameters.addTab(self.PathwayAnalysis, "")
        self.verticalLayout.addWidget(self.tabWidgetParameters)

        self.retranslateUi(ShowResultDlg)
        self.tabWidgetParameters.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(ShowResultDlg)

    def retranslateUi(self, ShowResultDlg):
        _translate = QtCore.QCoreApplication.translate
        ShowResultDlg.setWindowTitle(_translate("ShowResultDlg", "Dialog"))
        self.label.setText(_translate("ShowResultDlg", "Select/Input Cooling Period"))
        self.comboBoxDecayPeriod.setItemText(0, _translate("ShowResultDlg", "1"))
        self.comboBoxDecayPeriod.setItemText(1, _translate("ShowResultDlg", "2"))
        self.comboBoxDecayPeriod.setItemText(2, _translate("ShowResultDlg", "3"))
        self.comboBoxDecayPeriod.setItemText(3, _translate("ShowResultDlg", "4"))
        self.comboBoxDecayPeriod.setItemText(4, _translate("ShowResultDlg", "5"))
        self.tabWidgetParameters.setTabText(self.tabWidgetParameters.indexOf(self.Parameters), _translate("ShowResultDlg", "Parameters"))
        self.tabWidgetParameters.setTabText(self.tabWidgetParameters.indexOf(self.TransmutationGraph), _translate("ShowResultDlg", "Transmutation Graph"))
        self.tabWidgetParameters.setTabText(self.tabWidgetParameters.indexOf(self.PrimaryNuclides), _translate("ShowResultDlg", "Primary Nuclides"))
        self.tabWidgetParameters.setTabText(self.tabWidgetParameters.indexOf(self.PathwayAnalysis), _translate("ShowResultDlg", "Pathway Analysis"))

from widgetparam import WidgetParam
from widgetpathway import WidgetPathway
from widgetprimarynuclides import WidgetPrimaryNuclides
from widgettransgraph import WidgetTransGraph
