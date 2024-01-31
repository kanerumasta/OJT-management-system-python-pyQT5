from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Dialog(QDialog):
    def __init__(self,parent,dialog_type=None):
        super().__init__(parent)
        loadUi('Content/DialogWidget.ui', self)
        self.dialog_type = dialog_type
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) 
        self.setAttribute(Qt.WA_TranslucentBackground) 
        self.dialog_no_btn.clicked.connect(self.close)

        self.dialog_yes_btn.clicked.connect(self.action)

    def action(self):
        if self.dialog_type:
            if self.dialog_type.lower() == "logout":
                self.parent().stackedWidget.setCurrentIndex(0)
                self.close()





