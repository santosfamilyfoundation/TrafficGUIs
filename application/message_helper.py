"""
Project management classes and functions
"""

from PyQt5 import QtWidgets, QtCore
from views.message_dialog import Ui_message_dialog

class MessageHelper(QtWidgets.QDialog):

    def __init__(self, parent):
        super(MessageHelper, self).__init__(parent)
        self.ui = Ui_message_dialog()
        self.ui.setupUi(self)

        self.ui.close_button.clicked.connect(self.close)

        # Remove '?' icon
        flags = self.windowFlags() & (~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(flags)

    def show_message(self, message, title=None):
        self.ui.label.setText(message)

        if title is not None:
            self.setWindowTitle(title)

        self.adjustSize()
        self.show()

