# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message_dialog.ui'
#
# Created: Mon Feb 20 13:11:19 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_message_dialog(object):
    def setupUi(self, message_dialog):
        message_dialog.setObjectName(_fromUtf8("message_dialog"))
        message_dialog.resize(400, 292)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(message_dialog.sizePolicy().hasHeightForWidth())
        message_dialog.setSizePolicy(sizePolicy)
        message_dialog.setMaximumSize(QtCore.QSize(400, 16777215))
        self.gridLayout = QtGui.QGridLayout(message_dialog)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(message_dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText(_fromUtf8(""))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.close_button = QtGui.QPushButton(message_dialog)
        self.close_button.setObjectName(_fromUtf8("close_button"))
        self.verticalLayout.addWidget(self.close_button)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(message_dialog)
        QtCore.QMetaObject.connectSlotsByName(message_dialog)

    def retranslateUi(self, message_dialog):
        message_dialog.setWindowTitle(_translate("message_dialog", "Message", None))
        self.close_button.setText(_translate("message_dialog", "Close", None))

