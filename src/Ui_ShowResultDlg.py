# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ShowResultDlg.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ShowResultDlg(object):
    def setupUi(self, ShowResultDlg):
        ShowResultDlg.setObjectName("ShowResultDlg")
        ShowResultDlg.resize(900, 700)
        ShowResultDlg.setMinimumSize(QtCore.QSize(720, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(ShowResultDlg)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidgetParameters = QtWidgets.QTabWidget(ShowResultDlg)
        self.tabWidgetParameters.setObjectName("tabWidgetParameters")
        self.Parameters = WidgetParam()
        self.Parameters.setObjectName("Parameters")
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
        self.tabWidgetParameters.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ShowResultDlg)

    def retranslateUi(self, ShowResultDlg):
        _translate = QtCore.QCoreApplication.translate
        ShowResultDlg.setWindowTitle(_translate("ShowResultDlg", "Dialog"))
        self.tabWidgetParameters.setTabText(self.tabWidgetParameters.indexOf(self.Parameters), _translate("ShowResultDlg", "Activation Properties"))
        self.tabWidgetParameters.setTabText(self.tabWidgetParameters.indexOf(self.TransmutationGraph), _translate("ShowResultDlg", "Transmutation Graph"))
        self.tabWidgetParameters.setTabText(self.tabWidgetParameters.indexOf(self.PrimaryNuclides), _translate("ShowResultDlg", "Primary Nuclides"))
        self.tabWidgetParameters.setTabText(self.tabWidgetParameters.indexOf(self.PathwayAnalysis), _translate("ShowResultDlg", "Pathways"))

from widgetparam import WidgetParam
from widgetpathway import WidgetPathway
from widgetprimarynuclides import WidgetPrimaryNuclides
from widgettransgraph import WidgetTransGraph
