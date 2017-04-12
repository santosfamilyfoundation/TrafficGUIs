# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_project.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_choose_project(object):
    def setupUi(self, choose_project):
        choose_project.setObjectName("choose_project")
        choose_project.setEnabled(True)
        choose_project.resize(400, 150)
        choose_project.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.gridLayout = QtWidgets.QGridLayout(choose_project)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(choose_project)
        self.label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.create_new_project_button = QtWidgets.QPushButton(choose_project)
        self.create_new_project_button.setObjectName("create_new_project_button")
        self.horizontalLayout.addWidget(self.create_new_project_button)
        self.open_project_button = QtWidgets.QPushButton(choose_project)
        self.open_project_button.setObjectName("open_project_button")
        self.horizontalLayout.addWidget(self.open_project_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(choose_project)
        QtCore.QMetaObject.connectSlotsByName(choose_project)

    def retranslateUi(self, choose_project):
        _translate = QtCore.QCoreApplication.translate
        choose_project.setWindowTitle(_translate("choose_project", "Choose Project"))
        self.label.setText(_translate("choose_project", "Would you like to create a new project or open an existing one?"))
        self.create_new_project_button.setText(_translate("choose_project", "Create New Project"))
        self.open_project_button.setText(_translate("choose_project", "Open Project"))

