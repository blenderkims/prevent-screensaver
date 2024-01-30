from PyQt5 import QtWidgets
from window import MainWindow
import sys

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.show()
	mainWindow.enableButtonClick()
	sys.exit(app.exec_())