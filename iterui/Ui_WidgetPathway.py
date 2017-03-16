# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/WidgetPathway.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetPathway(object):
    def setupUi(self, WidgetPathway):
        WidgetPathway.setObjectName("WidgetPathway")
        WidgetPathway.resize(400, 300)
        WidgetPathway.setMinimumSize(QtCore.QSize(300, 300))
        self.horizontalLayout = QtWidgets.QHBoxLayout(WidgetPathway)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(WidgetPathway)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(WidgetPathway)
        QtCore.QMetaObject.connectSlotsByName(WidgetPathway)

    def retranslateUi(self, WidgetPathway):
        _translate = QtCore.QCoreApplication.translate
        WidgetPathway.setWindowTitle(_translate("WidgetPathway", "Form"))

