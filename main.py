# Main Application Program
import mainUI as ui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import image
from functools import partial

class phaseMonster(ui.Ui_MainWindow):
    # Main Application Class
    def __init__(self, starterWindow):
        super(phaseMonster, self).setupUi(starterWindow)
        self.mixer = image.mixer2Image()  # holds the mixer object from image.py
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

        self.showCmbxs = [self.image1Cmbx, self.image2Cmbx]
        self.componentCmbxs = [self.mixerCmbx1, self.mixerCmbx2]

        self.loadbtns = [self.img1Load, self.img2Load]

        # loop settings
        # imageView settings
        for img in self.imageWidgets:
            img.ui.histogram.hide()
            img.ui.roiBtn.hide()
            img.ui.menuBtn.hide()
            img.ui.roiPlot.hide()
            img.view.setBackgroundColor([255.0, 255.0, 255.0])

        # buttons settings
        for btn in self.loadbtns:
            btn.clicked.connect(partial(self.loadImage, btn.property('image')))

        for bx in self.showCmbxs:
            bx.activated.connect(partial(self.selectComponents, bx.property('image')))

        self.mixerOutput.activated.connect(self.chosenOutput())


    def loadImage(self, Indx: int):
        """
        maintains the loading of both images processes
        ============= =====================================================================
        **Arguments**
        Indx          an integer key to the image sent
        ============= =====================================================================
        """
        print(Indx)
        self.imageName, self.imageFormat = QtWidgets.QFileDialog.getOpenFileName(None, "Load Image %s" % Indx,
                                                                                 filter="*.jpg")
        if self.imageName == "":
            print("user cancelled loading")
            pass
        else:
            if Indx == 1:
                self.showImage(self.image1, self.imageOneOrigin, imageName= self.imageName)
                self.imageOneMods.clear()
                try:
                    self.selectComponents(Indx)
                except ValueError:  # this case happens when the user loads a different sized images
                    print("user loaded different sizes, image%s"%Indx)
                    pass
            elif Indx == 2:
                self.showImage(self.image2, self.imageTwoOrigin, imageName= self.imageName)
                self.imageTwoMods.clear()
                try:
                    self.selectComponents(Indx)
                except ValueError: # this case happens when the user loads a different sized images
                    print("user loaded different sizes, image %s "%Indx)
                    pass
            else:
                print("some Error")

    def selectComponents(self, image: int):
        if image == 1: self.showComponent(self.image1Cmbx.currentText(), self.image1, self.imageOneMods)
        elif image == 2 : self.showComponent(self.image2Cmbx.currentText(), self.image2, self.imageTwoMods)
        else: print("error here")

    def showComponent(self, mode: str, imageInst, widget, shifted :bool =True, checkShape: bool = False,
                      logScale:bool = True):
        """
        a case responsible function which routes the modes selected by user to be shown
        ============= =====================================================================
        **Arguments**
        mode:         the mode selected by user.
        imageInst:    the image modified.
        widget:       the widget to be set.
        shifted:      a boolean which shifts the fourier transform and get the phase.
        checkShape:   boolean to skip shape checking as it is done already.
        logScale:     a boolean which scales the required mod by 20 * log(component).
        ============= =====================================================================
        """
        imageInst.fourierTransform(shifted=shifted)
        if mode == 'Magnitude':
            self.showImage(imageInst, widget, checkShape=checkShape,
                           widgetData=imageInst.magnitude(logScale=logScale).T)

        if mode == "Phase":
            self.showImage(imageInst, widget, checkShape=checkShape,
                           widgetData= imageInst.phase(shifted=shifted).T)

        if mode == "Real Component":
            self.showImage(imageInst, widget, checkShape=checkShape,
                           widgetData= imageInst.realComponent(logScale).T)

        if mode == "Imaginary Component":
            self.showImage(imageInst, widget, checkShape=checkShape,
                           widgetData= imageInst.imaginaryComponent(logScale).T)

    def showImage(self, imageInst, widget, checkShape: bool = True, widgetData : bytearray = None, imageName: str =None):
        """
        Responsible for showing any image of any component in the specified widget
        ============= ===================================================================================
        **Arguments**
         imageInst:   the image class.
         widget:      the widget to be plotted to.
         checkShape:  boolean if True, checks the shape of the loaded images.
         widgetData:  a numpy array if exists will set the widget data to this array.
         imageName:   the path to the image if not none then the function load this image and plot it.
        ============= ===================================================================================
        """
        if imageName is not None: imageInst.loadImage(imageName)
        if widgetData is not None :
            widget.setImage(widgetData)
        else:
            widget.setImage(imageInst.imageData.T)

        widget.view.setAspectLocked(False)
        widget.view.setRange(xRange=[0, imageInst.imageShape[1]],
                             yRange=[0, imageInst.imageShape[0]], padding=0)
        print("done")
        if checkShape and self.image1.imageShape != self.image2.imageShape and self.image1.imageShape != None and self.image2.imageShape != None:
            self.showMessage("Warning", "You loaded two different sizes of images, Please choose another",
                             QMessageBox.Ok, QMessageBox.Warning)
            widget.clear()
            imageInst.clear()

    def chosenOutput(self):
        if self.mixerOutput.currentText() == "Output 1":
            pass
        elif self.mixerOutput.currentText() == "Output 2":
            pass
        else: print("Some error in output choosen")

    def showOutputMixed(self):
        pass

    def showMessage(self, header, message, button, icon):
        """
        responsible for showing message boxes
        ============= ===================================================================================
        **Arguments**
        header:       Box header title.
        message       the informative message to be shown.
        button:       button type.
        icon:         icon type.
        ============= ===================================================================================
        """
        msg = QMessageBox()
        msg.setWindowTitle(header)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(button)
        msg.exec_()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = phaseMonster(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

