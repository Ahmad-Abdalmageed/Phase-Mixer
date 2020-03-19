# Main Application Program
import mainUI as ui
from PyQt5 import QtCore, QtGui, QtWidgets


class phaseMonster(ui.Ui_MainWindow):
    # Main Application Class
    pass



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = phaseMonster()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

