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
        self.out1 = image.image()
        self.out2 = image.image()
        self.imagesShapes = []  # holds images shapes loaded to be checked
        self.images = [self.image1, self.image2]  # not used may be deleted later

        # UI components
        self.imageWidgets = [self.imageOneOrigin, self.imageTwoOrigin, self.imageOneMods, self.imageTwoMods,
                             self.output1, self.output2]
        self.sliders = [self.slider1, self.slider2]
        self.cmbxs = [self.image1Cmbx, self.image2Cmbx, self.mixerOutput, self.mixerCmbx1, self.mixerCmbx2,
                      self.component1, self.component2]  # not used maybe deleted later
        self.showCmbxs = [self.image1Cmbx, self.image2Cmbx]

        self.mixerCmbxs = [self.mixerCmbx1, self.mixerCmbx2]
        self.componentCmbxs = [self.component1, self.component2]

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

        self.mixerOutput.currentTextChanged.connect(partial(self.chosenOutput, 0))

        for index, mxrbx in enumerate(self.mixerCmbxs):
            mxrbx.currentTextChanged.connect(partial(self.chosenOutput, index))

        for index, component in enumerate(self.componentCmbxs):
            component.currentTextChanged.connect(partial(self.chosenOutput, index))

        for index, slider in enumerate(self.sliders):
            slider.valueChanged.connect(partial(self.chosenOutput, index))

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
                self.mixer.deleteImage(0)
                self.mixer.addImage(self.image1)
                self.imageOneMods.clear()
                self.chosenOutput(0)
                try:
                    self.selectComponents(Indx)
                except ValueError:  # this case happens when the user loads a different sized images
                    print("user loaded different sizes, image%s"%Indx)
                    pass
            elif Indx == 2:
                self.showImage(self.image2, self.imageTwoOrigin, imageName= self.imageName)
                self.mixer.deleteImage(1)
                self.mixer.addImage(self.image2, shifted=True)
                self.imageTwoMods.clear()
                self.chosenOutput(0)
                try:
                    self.selectComponents(Indx)
                except ValueError: # this case happens when the user loads a different sized images
                    print("user loaded different sizes, image %s "%Indx)
                    pass
            else:
                print("some Error")

    def selectComponents(self, image: int):
        """
        Masking Fucntion which routes the user choice of component to be shown to the showing functions
        ============= =====================================================================
        **Arguments**
        image         an integer indicating which image is chosen
        ============= =====================================================================
        """
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
        if imageName is not None: imageInst.loadImage(path = imageName)
        if widgetData is not None :
            widget.setImage(widgetData)
        else:
            widget.setImage(imageInst.imageData.T)

        widget.view.setAspectLocked(False)
        widget.view.setRange(xRange=[0, imageInst.imageShape[1]],
                             yRange=[0, imageInst.imageShape[0]], padding=0)

        if checkShape and self.image1.imageShape != self.image2.imageShape and \
                self.image1.imageShape != None and self.image2.imageShape != None:
            self.showMessage("Warning", "You loaded two different sizes of images, Please choose another",
                             QMessageBox.Ok, QMessageBox.Warning)
            widget.clear()
            imageInst.clear()

    def chosenOutput(self, component: int):
        try:
            if self.mixerOutput.currentText() == "Output 1":
                self.out1.loadImage(fourier= self.__mixer(component), imageShape=self.image1.imageShape)
                self.out1.inverseFourier()
                self.showImage(self.out1, self.output1, False, self.out1.imageFourierInv.T)

            elif self.mixerOutput.currentText() == "Output 2":
                self.out2.loadImage(fourier= self.__mixer(component), imageShape=self.image1.imageShape)
                self.out2.inverseFourier()
                self.showImage(self.out2, self.output2, False, self.out2.imageFourierInv.T)

            else: print("Some error in output chosen")
        except IndexError:
            self.showMessage("Warning", "You did not load any image", QMessageBox.Ok, QMessageBox.Warning)
            pass
    def showMessage(self, header, message, button, icon):
        """
        Responsible for showing message boxes
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

    def __mixer(self, component: int) -> "numpy.ndarray":

        if self.componentCmbxs[component].currentText() == "Magnitude" or self.componentCmbxs[component].currentText() == "Phase":
            self.componentCmbxs[~component].setCurrentIndex(0)

            print(self.mixerCmbxs[component].currentIndex())
            print(self.mixerCmbxs[~component].currentIndex())

            return self.mixer.mix(self.sliders[0].value()/10, self.sliders[1].value()/10,
                           self.mixerCmbxs[component].currentIndex(),
                           mode= image.Modes.magnitudePhase)

        if self.componentCmbxs[component].currentText() == "Real Component" or self.componentCmbxs[component].currentText() == "Imaginary Component":

            print(self.mixerCmbxs[component].currentIndex())
            print(self.mixerCmbxs[~component].currentIndex())

            self.componentCmbxs[~component].setCurrentIndex(1)

            return self.mixer.mix(self.sliders[component].value()/10, self.sliders[~component].value()/10,
                                  self.mixerCmbxs[component].currentIndex(),
                                  mode=image.Modes.realImaginary)

        if self.component1.currentText() == "Uniform Magnitude":
            pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = phaseMonster(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

