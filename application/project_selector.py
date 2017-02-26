"""
Project management classes and functions
"""

from PyQt5 import QtWidgets, QtCore
from choose_project import Ui_choose_project

class ProjectSelectionWizard(QtWidgets.QDialog):

    def __init__(self, parent):
        super(ProjectSelectionWizard, self).__init__(parent)
        self.ui = Ui_choose_project()
        self.ui.setupUi(self)

        self.ui.create_new_project_button.clicked.connect(self.create_new_project)
        self.ui.open_project_button.clicked.connect(self.open_project)

        # Remove '?' icon
        flags = self.windowFlags() & (~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(flags)

    def create_new_project(self):
        self.parent().create_new_project()
        self.close()

    def open_project(self):
        self.parent().open_project()
        self.close()

