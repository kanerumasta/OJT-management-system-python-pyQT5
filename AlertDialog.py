from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class AlertDialog(QDialog):
    def __init__(self,parent,alert_type="error", message="Error"):
        super().__init__(parent)
        loadUi('Content/alert.ui', self)
        self.alert_type = alert_type
        self.message = message
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Additional window flags for customization
        self.setAttribute(Qt.WA_TranslucentBackground) 
        self.alert_changeable_message.setText(message)
        self.alert_ok_button.clicked.connect(lambda:self.close())

        if alert_type.lower() == "error":
            self.error_style()
           
        elif alert_type.lower() == "success":
            self.success_style()
        elif alert_type.lower() == "warning":
            self.warning_style()
            

    def error_style(self):
        self.alert_colored_frame.setStyleSheet("background-color: rgb(255, 80, 92);border-radius:10px;")
        self.alert_type_label.setText(self.alert_type.upper()+"!")
        self.alert_type_label.setStyleSheet("background-color:transparent;color: rgb(100, 100, 100);font-size:26px")
        self.alert_changeable_message.setText(self.message)
        self.alert_changeable_message.setStyleSheet("background-color:transparent;color: rgb(100, 100, 100);")
        self.alert_icon.setPixmap(QPixmap(":/icons/icons/pngwing.com.png"))
        self.alert_ok_button.setStyleSheet("""#alert_ok_button{
                                            border:none;
                                                background-color: rgb(255, 80, 92);
                                            border-radius:10px;
                                            color:#fff;
                                                }
                                              
                                                #alert_ok_button:hover{
                                                    background-color: rgba(255, 80, 92, 190);
                                                }""")

    def success_style(self):
        self.alert_colored_frame.setStyleSheet("background-color: #00b585;border-radius:10px;")
        self.alert_type_label.setText(self.alert_type.upper()+"!")
        self.alert_type_label.setStyleSheet("background-color:transparent;color: rgb(100, 100, 100);font-size:26px")
        self.alert_changeable_message.setStyleSheet("background-color:transparent;color: rgb(100, 100, 100);")
        self.alert_changeable_message.setText(self.message)
        self.alert_ok_button.setStyleSheet("""#alert_ok_button{
                                            border:none;
                                                    background-color: #00b585;
                                                border-radius:10px;
                                                color:#fff;
                                                }
                                              
                                                #alert_ok_button:hover{
                                                    background-color: rgba(0, 181, 133, 190);
                                                }""")
        self.alert_icon.setPixmap(QPixmap(":/icons/icons/800px-Sign-check-icon.png"))
    def warning_style(self):
        self.alert_colored_frame.setStyleSheet("background-color:#e9b82c;border-radius:10px;")
        self.alert_type_label.setText(self.alert_type.upper()+"!")
        self.alert_type_label.setStyleSheet("background-color:transparent;color: rgb(100, 100, 100);font-size:26px")
        self.alert_changeable_message.setStyleSheet("background-color:transparent;color: rgb(100, 100, 100);")
        self.alert_changeable_message.setText(self.message)
        self.alert_ok_button.setStyleSheet("""#alert_ok_button{
                                            border:none;
                                                    background-color: #e9b82c;
                                                border-radius:10px;
                                                color:#fff;
                                                }
                                              
                                                #alert_ok_button:hover{
                                                    background-color: rgba(233, 184,44, 190);
                                                }""")
        self.alert_icon.setPixmap(QPixmap(":/icons/icons/warning.png"))

    
