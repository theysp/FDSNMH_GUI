# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WidgetParam.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetParam(object):
    def setupUi(self, WidgetParam):
        WidgetParam.setObjectName("WidgetParam")
        WidgetParam.resize(539, 432)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(WidgetParam)
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tabWidgetDisplay = QtWidgets.QTabWidget(WidgetParam)
        self.tabWidgetDisplay.setObjectName("tabWidgetDisplay")
        self.Data = QtWidgets.QWidget()
        self.Data.setObjectName("Data")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.Data)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableParams = QtWidgets.QTableView(self.Data)
        self.tableParams.setMinimumSize(QtCore.QSize(300, 300))
        self.tableParams.setObjectName("tableParams")
        self.verticalLayout_3.addWidget(self.tableParams)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonSaveParam = QtWidgets.QPushButton(self.Data)
        self.pushButtonSaveParam.setObjectName("pushButtonSaveParam")
        self.horizontalLayout.addWidget(self.pushButtonSaveParam)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.tabWidgetDisplay.addTab(self.Data, "")
        self.Plot = QtWidgets.QWidget()
        self.Plot.setObjectName("Plot")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Plot)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.framePlot = QtWidgets.QFrame(self.Plot)
        self.framePlot.setMinimumSize(QtCore.QSize(0, 300))
        self.framePlot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePlot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framePlot.setObjectName("framePlot")
        self.verticalLayout_4.addWidget(self.framePlot)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButtonSavePlot = QtWidgets.QPushButton(self.Plot)
        self.pushButtonSavePlot.setObjectName("pushButtonSavePlot")
        self.horizontalLayout_2.addWidget(self.pushButtonSavePlot)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.tabWidgetDisplay.addTab(self.Plot, "")
        self.horizontalLayout_3.addWidget(self.tabWidgetDisplay)

        self.retranslateUi(WidgetParam)
        self.tabWidgetDisplay.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(WidgetParam)

    def retranslateUi(self, WidgetParam):
        _translate = QtCore.QCoreApplication.translate
        WidgetParam.setWindowTitle(_translate("WidgetParam", "Form"))
        self.pushButtonSaveParam.setText(_translate("WidgetParam", "Save"))
        self.tabWidgetDisplay.setTabText(self.tabWidgetDisplay.indexOf(self.Data), _translate("WidgetParam", "Data"))
        self.pushButtonSavePlot.setText(_translate("WidgetParam", "Save"))
        self.tabWidgetDisplay.setTabText(self.tabWidgetDisplay.indexOf(self.Plot), _translate("WidgetParam", "Plot"))

