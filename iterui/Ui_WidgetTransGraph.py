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
        WidgetTransGraph.resize(561, 462)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(WidgetTransGraph)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.framePlot = QtWidgets.QFrame(WidgetTransGraph)
        self.framePlot.setMinimumSize(QtCore.QSize(300, 300))
        self.framePlot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framePlot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framePlot.setObjectName("framePlot")
        self.verticalLayout_2.addWidget(self.framePlot)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonSavePlot = QtWidgets.QPushButton(WidgetTransGraph)
        self.pushButtonSavePlot.setObjectName("pushButtonSavePlot")
        self.horizontalLayout.addWidget(self.pushButtonSavePlot)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(WidgetTransGraph)
        QtCore.QMetaObject.connectSlotsByName(WidgetTransGraph)

    def retranslateUi(self, WidgetTransGraph):
        _translate = QtCore.QCoreApplication.translate
        WidgetTransGraph.setWindowTitle(_translate("WidgetTransGraph", "Form"))
        self.pushButtonSavePlot.setText(_translate("WidgetTransGraph", "Save"))

