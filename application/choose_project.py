# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_project.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_choose_project(object):
    def setupUi(self, choose_project):
        choose_project.setObjectName(_fromUtf8("choose_project"))
        choose_project.setEnabled(True)
        choose_project.resize(400, 150)
        choose_project.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.gridLayout = QtGui.QGridLayout(choose_project)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(choose_project)
        self.label.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.create_new_project_button = QtGui.QPushButton(choose_project)
        self.create_new_project_button.setObjectName(_fromUtf8("create_new_project_button"))
        self.horizontalLayout.addWidget(self.create_new_project_button)
        self.open_project_button = QtGui.QPushButton(choose_project)
        self.open_project_button.setObjectName(_fromUtf8("open_project_button"))
        self.horizontalLayout.addWidget(self.open_project_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(choose_project)
        QtCore.QMetaObject.connectSlotsByName(choose_project)

    def retranslateUi(self, choose_project):
        choose_project.setWindowTitle(_translate("choose_project", "Choose Project", None))
        self.label.setText(_translate("choose_project", "Would you like to create a new project or open an existing one?", None))
        self.create_new_project_button.setText(_translate("choose_project", "Create New Project", None))
        self.open_project_button.setText(_translate("choose_project", "Open Project", None))
