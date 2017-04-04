# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/WidgetPathway.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetPathway(object):
    def setupUi(self, WidgetPathway):
        WidgetPathway.setObjectName("WidgetPathway")
        WidgetPathway.resize(814, 445)
        WidgetPathway.setMinimumSize(QtCore.QSize(300, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(WidgetPathway)
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(WidgetPathway)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.plainTextEditSearchNuclide = QtWidgets.QPlainTextEdit(WidgetPathway)
        self.plainTextEditSearchNuclide.setMaximumSize(QtCore.QSize(16777215, 25))
        self.plainTextEditSearchNuclide.setObjectName("plainTextEditSearchNuclide")
        self.horizontalLayout_2.addWidget(self.plainTextEditSearchNuclide)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidgetPathway = QtWidgets.QTableWidget(WidgetPathway)
        self.tableWidgetPathway.setObjectName("tableWidgetPathway")
        self.tableWidgetPathway.setColumnCount(3)
        self.tableWidgetPathway.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetPathway.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetPathway.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetPathway.setHorizontalHeaderItem(2, item)
        self.tableWidgetPathway.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidgetPathway.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetPathway.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidgetPathway)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonSave = QtWidgets.QPushButton(WidgetPathway)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.horizontalLayout.addWidget(self.pushButtonSave)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(WidgetPathway)
        QtCore.QMetaObject.connectSlotsByName(WidgetPathway)

    def retranslateUi(self, WidgetPathway):
        _translate = QtCore.QCoreApplication.translate
        WidgetPathway.setWindowTitle(_translate("WidgetPathway", "Form"))
        self.label.setText(_translate("WidgetPathway", "Search Target Nuclides"))
        item = self.tableWidgetPathway.horizontalHeaderItem(0)
        item.setText(_translate("WidgetPathway", "Target Nuclide"))
        item = self.tableWidgetPathway.horizontalHeaderItem(1)
        item.setText(_translate("WidgetPathway", "Proportion"))
        item = self.tableWidgetPathway.horizontalHeaderItem(2)
        item.setText(_translate("WidgetPathway", "Pathway"))
        self.pushButtonSave.setText(_translate("WidgetPathway", "Save"))

