# Main Application Program
import mainUI as ui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import image
from functools import partial
import logging

class phaseMonster(ui.Ui_MainWindow):
    # Main Application Class
    def __init__(self, starterWindow):
        super(phaseMonster, self).setupUi(starterWindow)
        self.imageName = None  # holds image path
        self.imageFormat = None  # holds image format
        self.mixer = image.mixer2Image()  # holds the mixer object from image.py
        self.image1 = image.image()  # holds the image object from image.py
        self.image2 = image.image()  # holds the image object from image.py
        self.out1 = image.image()  # holds the image object of the first output
        self.out2 = image.image()  # holds the image object of the second output
        self.imagesShapes = []  # holds images shapes loaded to be checked
        self.images = [self.image1, self.image2]  # not used may be deleted later
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # UI components
        self.imageWidgets = [self.imageOneOrigin, self.imageTwoOrigin, self.imageOneMods, self.imageTwoMods,
                             self.output1, self.output2]

        self.sliders = [self.slider1, self.slider2]

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

        self.mixerOutput.currentTextChanged.connect(self.chosenOutput)

        for index, mxrbx in enumerate(self.mixerCmbxs):
            mxrbx.currentTextChanged.connect(self.chosenOutput)
            mxrbx.currentTextChanged.connect(self.setComponents)

        for index, component in enumerate(self.componentCmbxs):
            component.currentTextChanged.connect(self.chosenOutput)

        for index, slider in enumerate(self.sliders):
            slider.valueChanged.connect(self.chosenOutput)

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

        self.logger.debug("image from:%s"%self.imageName)
        if self.imageName == "":
            self.logger.debug("loading cancelled")
            pass
        else:
            if Indx == 1:
                self.__loadImage(self.image1, self.imageOneOrigin, self.imageOneMods, self.imageName, 1,True)
                self.logger.debug("loading done")

                try:
                    self.selectComponents(Indx)
                except ValueError:  # this case happens when the user loads a different sized images
                    print("user loaded different sizes, image%s"%Indx)
                    pass

            elif Indx == 2:
                self.__loadImage(self.image2, self.imageTwoOrigin, self.imageTwoMods, self.imageName, 2,True)
                try:
                    self.selectComponents(Indx)
                except ValueError: # this case happens when the user loads a different sized images
                    print("user loaded different sizes, image %s "%Indx)
                    pass
            else:
                print("some Error") # may not be executed

    def __loadImage(self, imageInst: image.image, widget: "pyqtgraph.ImageView", clearedWid: "pyqtgraph.ImageView",
                    path: str, indx: int, shifted: bool = False):
        """
        A mask for loadImage
        """
        try:
            self.showImage(imageInst, widget, imageName=path)
            self.mixer.deleteImage(indx-1)
            self.mixer.addImage(imageInst, shifted=shifted)
            clearedWid.clear()
            self.chosenOutput()

        except ValueError:
            print("user loaded different sizes")
            pass

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
        self.logger.debug("selected %s to be shown for %s" % (mode, widget.name))
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
        self.logger.debug("%s widget data set"% widget.name)

        if checkShape and self.image1.imageShape != self.image2.imageShape and \
                self.image1.imageShape != None and self.image2.imageShape != None:
            self.showMessage("Warning", "You loaded two different sizes of images, Please choose another",
                             QMessageBox.Ok, QMessageBox.Warning)
            self.logger.debug("different sizes loaded")
            widget.clear()
            imageInst.clear()

    def chosenOutput(self):
        """
        Called on amy change in ui mixer part.
        Implements the following:
        * checks for which output is chosen
        * route the the mixer values to the widget and set it`s data
        """
        try:
            if self.mixerOutput.currentText() == "Output 1":
                self.__chosenOutput(self.out1, self.image1.imageShape, self.output1)

            elif self.mixerOutput.currentText() == "Output 2":
                self.__chosenOutput(self.out2, self.image1.imageShape, self.output2)

            else: print("Some error in output chosen")

        except IndexError:
            self.showMessage("Heads Up", "Please Load another image for comparing part", QMessageBox.Ok, QMessageBox.Warning)
            pass

    def __chosenOutput(self, outInst: image.image, imageShape, widget: "pyqtgraph.ImageView", checkShape:bool = False):
        """
        A mask for chosenOutput
        """
        outInst.loadImage(fourier=self.__mixer(), imageShape=imageShape)
        outInst.inverseFourier()
        self.showImage(outInst, widget, checkShape, outInst.imageFourierInv.T)
        self.logger.debug("output drawn")

    def setComponents(self):
        """
        Checks user choices and correct them
        """
        if self.componentCmbxs[0].currentText() == "Magnitude":
            self.componentCmbxs[1].setCurrentIndex(0)
        if self.componentCmbxs[0].currentText() == "Real Component" :
            self.componentCmbxs[1].setCurrentIndex(1)

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
        self.logger.debug("messege shown with %s %s "%(header, message))
        msg.exec_()

    def __mixer(self) -> "numpy.ndarray":
        """
        Main mixing function
        """
        self.setComponents()
        if self.componentCmbxs[0].currentText() == "Magnitude" or self.componentCmbxs[1].currentText() == "Phase":
            print("MG/PH mode")
            self.logger.debug("mode chosen Mg/Ph")

            if self.componentCmbxs[0].currentText() == "Uniform Magnitude" or self.componentCmbxs[1].currentText() == "Uniform Phase":
                self.logger.debug("uniform mode chosen")
                return self.mixer.mix(self.sliders[0].value() / 10, self.sliders[1].value() / 10,
                               self.mixerCmbxs[0].currentIndex(), self.mixerCmbxs[1].currentIndex(),
                               image.Modes.magnitudePhase, self.componentCmbxs[0].currentText()=="Uniform Magnitude",
                               self.componentCmbxs[1].currentText() == "Uniform Phase")

            return self.mixer.mix(self.sliders[0].value()/10, self.sliders[1].value()/10,
                           self.mixerCmbxs[0].currentIndex(), self.mixerCmbxs[1].currentIndex(), mode=image.Modes.magnitudePhase)

        if self.componentCmbxs[1].currentText() == "Imaginary Component" or self.componentCmbxs[0].currentText() == "Real Component":
            self.logger.debug("R/I mode")
            return self.mixer.mix(self.sliders[0].value()/10, self.sliders[1].value()/10,
                           self.mixerCmbxs[0].currentIndex(), self.mixerCmbxs[1].currentIndex(), mode=image.Modes.realImaginary)
        self.showMessage("Heads up", "Choose a valid mode",QMessageBox.Ok, QMessageBox.Warning)



if __name__ == "__main__":
    import sys

    logging.basicConfig(filename="logs/logfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = phaseMonster(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

