# Main Application Program
import mainUI as ui
from PyQt5 import QtCore, QtGui, QtWidgets
import image
import cv2
import pyqtgraph as pg


class phaseMonster(ui.Ui_MainWindow):
    # Main Application Class
    def __init__(self, starterWindow):
        super(phaseMonster, self).setupUi(starterWindow)
        self.mixer = None # holds the mixer class from image.py




















        # # pg.setConfigOption('imageAxisOrder', 'row-major')
        # self.img = cv2.imread("TestImages/lelouch_lamperouge_code_geass_zero_102069_1920x1080.jpg")[:, :, 0]
        # print(self.img.ndim)
        # print(self.img.T.shape)
        # print(self.img.dtype)
        #
        # self.imageTwoOrigin.setImage(self.img.T, autoHistogramRange=True)
        #
        # self.imageTwoOrigin.view.setAspectLocked(False)
        # self.imageTwoOrigin.view.setRange(xRange=[0, self.img.T.shape[0]], yRange=[0, self.img.T.shape[1]], padding=0)
        # self.imageTwoOrigin.ui.histogram.hide()
        # self.imageTwoOrigin.ui.roiBtn.hide()
        # self.imageTwoOrigin.ui.menuBtn.hide()
        # self.imageTwoOrigin.ui.roiPlot.hide()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = phaseMonster(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    #
    # import pyqtgraph.examples
    #
    # pyqtgraph.examples.run()

