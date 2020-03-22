# Main Application Program
import mainUI as ui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import image
from functools import partial


class phaseMonster(ui.Ui_MainWindow):
    # Main Application Class
    def __init__(self, starterWindow):
        super(phaseMonster, self).setupUi(starterWindow)
        self.mixer = image.mixer2Image  # holds the mixer object from image.py
        self.image1 = image.image()  # holds the image object from image.py
        self.image2 = image.image()  # holds the image object from image.py
        self.imagesShapes = []  # holds images shapes loaded to be checked
        self.images = [self.image1, self.image2]  # not used may be deleted later

        # UI components
        self.imageWidgets = [self.imageOneOrigin, self.imageTwoOrigin, self.imageOneMods, self.imageTwoMods,
                             self.output1, self.output2]
        self.sliders = [self.component1, self.component2]
        self.cmbxs = [self.image1Cmbx, self.image2Cmbx, self.mixerOutput, self.mixerCmbx1, self.mixerCmbx2,
                      self.component1, self.component2]

        self.modCmbxs = [self.image1Cmbx, self.image2Cmbx]
        self.componentCmbxs = [self.mixerCmbx1, self.mixerCmbx2]

        self.loadbtns = [self.img1Load, self.img2Load]

        # loop settings
        # imageView settigs
        for img in self.imageWidgets:
            img.ui.histogram.hide()
            img.ui.roiBtn.hide()
            img.ui.menuBtn.hide()
            img.ui.roiPlot.hide()
            img.view.setBackgroundColor([255.0, 255.0, 255.0])
        # buttons settigns
        for btn in self.loadbtns:
            btn.clicked.connect(partial(self.loadImage, btn.property('image')))

    def loadImage(self, image: int):
        """
        maintains the loading of both images processes
        :return: None
        """
        print(image)
        self.imageName, self.imageFormat = QtWidgets.QFileDialog.getOpenFileName(None, "Load Image %s" % image,
                                                                                 filter="*.jpg")
        if self.imageName == "":
            pass
        else:
            if image == 1:
                self.showImage(self.image1, self.imageOneOrigin, self.imageName)

            elif image == 2:
                self.showImage(self.image2, self.imageTwoOrigin, self.imageName)

            else:
                print("some Error")

    def showImage(self, imageInst, widget, imageName):
        """
        responsible for loading the image in the specified widget
        """
        imageInst.loadImage(imageName)
        widget.setImage(imageInst.imageData.T)
        widget.view.setAspectLocked(False)
        widget.view.setRange(xRange=[0, imageInst.imageShape[1]]
                             , yRange=[0, imageInst.imageShape[0]], padding=0)

        if self.image1.imageShape != self.image2.imageShape and self.image1.imageShape != None and self.image2.imageShape != None:
            self.showMessage("Warning", "You loaded two different sizes of images, Please choose another",
                             QMessageBox.Ok, QMessageBox.Warning)
            widget.clear()
            imageInst.clear()


    def showMessage(self, header, message, button, icon):
        """
        responsible for showing message boxes
        :param header:Box header title
        :param message: the informative message to be shown
        :param button: button type
        :param icon: icon type
        :return: None
        """
        msg = QMessageBox()
        msg.setWindowTitle(header)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(button)
        msg.exec_()

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
