# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/WidgetTransGraph.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetTransGraph(object):
    def setupUi(self, WidgetTransGraph):
        WidgetTransGraph.setObjectName("WidgetTransGraph")
        WidgetTransGraph.resize(786, 455)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(WidgetTransGraph)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.framePlot = QtWidgets.QFrame(WidgetTransGraph)
        self.framePlot.setMinimumSize(QtCore.QSize(300, 300))
        self.framePlot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePlot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framePlot.setObjectName("framePlot")
        self.horizontalLayout_2.addWidget(self.framePlot)
        self.tableWidget = QtWidgets.QTableWidget(WidgetTransGraph)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(130, 16777215))
        self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tableWidget.setAutoScrollMargin(0)
        self.tableWidget.setGridStyle(QtCore.Qt.DashLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(40)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(0)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(WidgetTransGraph)
        QtCore.QMetaObject.connectSlotsByName(WidgetTransGraph)

    def retranslateUi(self, WidgetTransGraph):
        _translate = QtCore.QCoreApplication.translate
        WidgetTransGraph.setWindowTitle(_translate("WidgetTransGraph", "Form"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("WidgetTransGraph", "Nuclide"))

