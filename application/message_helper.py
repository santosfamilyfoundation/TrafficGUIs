"""
Project management classes and functions
"""

from PyQt4 import QtGui, QtCore
from views.message_dialog import Ui_message_dialog

class MessageHelper(QtGui.QDialog):

    def __init__(self, parent):
        super(MessageHelper, self).__init__(parent)
        self.ui = Ui_message_dialog()
        self.ui.setupUi(self)

        self.ui.close_button.clicked.connect(self.close)

        # Remove '?' icon
        flags = self.windowFlags() & (~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(flags)

    def show_message(self, message):
        self.ui.label.setText(message)
        self.show()

