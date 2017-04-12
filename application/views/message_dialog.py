# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_message_dialog(object):
    def setupUi(self, message_dialog):
        message_dialog.setObjectName("message_dialog")
        message_dialog.resize(400, 292)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(message_dialog.sizePolicy().hasHeightForWidth())
        message_dialog.setSizePolicy(sizePolicy)
        message_dialog.setMaximumSize(QtCore.QSize(400, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(message_dialog)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(message_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.close_button = QtWidgets.QPushButton(message_dialog)
        self.close_button.setObjectName("close_button")
        self.verticalLayout.addWidget(self.close_button)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(message_dialog)
        QtCore.QMetaObject.connectSlotsByName(message_dialog)

    def retranslateUi(self, message_dialog):
        _translate = QtCore.QCoreApplication.translate
        message_dialog.setWindowTitle(_translate("message_dialog", "Message"))
        self.close_button.setText(_translate("message_dialog", "Close"))

