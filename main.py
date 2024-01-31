from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import psycopg2
from MainWindow import MainWindow


def main():
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()


if __name__ == "__main__":
	main()
 		