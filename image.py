# This is the file which contains the image class
import cv2 as cv
import numpy as np
from typing import  Union
import enum

class Modes(enum.Enum):
    magnitudePhase = "magnitudePhaseMod"
    realImaginary = "realImaginaryMod"

class image():
    """
    Responsible for all interactions with a Grey Scale image.
    Implements the following:
    * Loading the image data to the class
    * Apply Fourier Transformation to the image
    * Extract the following components from the transformations :
        - Real Component
        - Imaginary Component
        - Phase
        - Magnitude

    Note: the image is transformed on loading to Grey scale
    """
    def __init__(self):
        """
        Initializing all Image Attributes
        """
        self.imageData = None  # image array
        self.imageFourier = None  # Fourier Transformation
        self.imageFourierShifted = None  # Shifted Fourier
        self.imageFourierInv = None  # Fourier Inverse
        self.imageFourierInvShifted = None # Shifted Fourier Inverse
        self.dataType = None  # The image data type
        self.imageShape = None  # the image shape
        self.__epsilon = 10**-8  # a value used to avoid dividing by zero

    def loadImage(self, path: str= None, data: np.ndarray = None, fourier: np.ndarray= None, imageShape : tuple= None):
        """
        Implements the following:
        * Loading the image from specified path
        * Normalize the image values
        * Converting to Grey Scale
        ================== ===========================================================================
        **Parameters**
        Path               a string specifying the absolute path to image
        ================== ===========================================================================
        """
        if data is not None:
            self.imageData = data
            self.imageShape= imageShape
            print("instance made with sent data")

        elif fourier is not None:
            self.imageFourier = fourier
            self.imageShape = imageShape
            print("image is set with transformed data")
        else:
            if path is not None:
                self.imageData = cv.imread(path)
                self.imageData = cv.cvtColor(self.imageData, cv.COLOR_RGB2GRAY)/255.0
                self.dataType = self.imageData.dtype
                self.imageShape = self.imageData.shape
                print("the image loaded shape is ", self.imageShape)
            else: print("No Given path"); pass

    def clear(self):
        """
        clear all data in image object
        """
        self.__init__()

    def fourierTransform(self, shifted: bool = False):
        """
        Applies Fourier Transform on the data of the image and save it in the specified attribute
        ================== ===========================================================================
        **Parameters**
        shifted            If True will also apply the shifted Fourier Transform
        ================== ===========================================================================
        """
        self.imageFourier = np.fft.fft2(self.imageData)
        if shifted: self.imageFourierShifted = np.fft.fftshift(self.imageFourier)

    def inverseFourier(self, shifted: bool = False):
        """
        Applies Inverse Fourier Transform on the image Fourier`s data and save it in specified attribute
        """
        self.imageFourierInv = np.real(np.fft.ifft2(self.imageFourier))
        # if shifted : self.imageFourierInvShifted = np.fft.ifft2(self.imageFourierShifted)

    def realComponent(self, logScale: bool = False):
        """
        Extracts the image`s Real Component from the image`s Fourier data
        ================== ===========================================================================
        **Parameters**
        LodScale           If true returns 20 * np.log(ImageFourier)
        ================== ===========================================================================
        **Returns**
        array              a numpy array of the extracted data
        ================== ===========================================================================
        """
        if logScale : return 20*np.log(np.real(self.imageFourier)+ self.__epsilon)
        else: return np.real(self.imageFourier)

    def imaginaryComponent(self, logScale:bool = False):
        """
        Extracts the image`s Imaginary Component from the image`s Fourier data
        ================== ===========================================================================
        **Parameters**
        LodScale           If true returns 20 * np.log(ImageFourier)
        ================== ===========================================================================
        **Returns**
        array              a numpy array of the extracted data
        ================== ===========================================================================
        """

        if logScale :return 20*np.log(np.imag(self.imageFourier)+self.__epsilon)
        else: return np.imag(self.imageFourier)

    def magnitude(self, logScale:bool = False):
        """
        Extracts the image`s Magnitude Spectrum from the image`s Fourier data
        ================== ===========================================================================
        **Parameters**
        LodScale           If true returns 20 * np.log(ImageFourier)
        ================== ===========================================================================
        **Returns**
        array              a numpy array of the extracted data
        ================== ===========================================================================
        """
        if logScale : return 20*np.log(np.abs(self.imageFourier))
        else: return np.abs(self.imageFourier)

    def phase(self, shifted: bool = False):
        """
        Extracts the image`s Phase Spectrum from the image`s Fourier data
        ================== ===========================================================================
        **Parameters**
        shifted           If true applies a phase shift on the returned data
        ================== ===========================================================================
        **Returns**
        array              a numpy array of the extracted data
        ================== ===========================================================================
        """
        if shifted : return np.angle(self.imageFourierShifted)
        else: return np.angle(self.imageFourier)


class mixer2Image():
    """
    Responsible for mixing images components extracted from the image`s Fourier Transform.
    Implements the following:
    * Add images either with a list of Image instances of just one instance
    * Mix with two modes:
        - Real and Imaginary mix.
        - Phase and Magnitude mix .
    """
    def __init__(self):
        """
        Initialize needed attributes for the class
        """
        self.imagesTransformed = []  # contains all instances of Image added
        self.realComponents = []  # Holds extracted Real Component from Image
        self.imaginaryComponents = []  # Holds extracted Imaginary Component from Image
        self.imagesPhase = []  # Holds Extracted Phase Spectrum from Image
        self.imagesMagnitude = []  # Holds Extracted Magnitude Spectrum from Image

    def addImage(self, image: Union[image, list], shifted: bool = False):
        """
        Add inserted Image instances to the class either by a list or one Instance
        ================== ===========================================================================
        **Parameters**
        image              A list of Image instances of just one instance
        shifted            If true returns components of a shifted fourier transform
        ================== ===========================================================================
        """
        if isinstance(image, list):
            for i in image:
                self.__addImage(i, shifted)
        else:
            self.__addImage(image, shifted)

    def mix(self, w1: float, w2: float, img1: int, img2:int, mode: Modes):
        """
        The mask mixing function which routes the user to the mode mixing functions according to the mode provided.
        Implements the following:
        * Takes a mode Enum from user:
            - Modes.magnitudePhase: which is the mode of applying the magnitude phase mix.
            - Modes.realImaginary: which is the mode of applying the real imaginary mix.
        ================== ===========================================================================
        **Parameters**
        w1                 (Float) first ratio
        w2                 (Float) Second ratio
        img                (int) which is the image to apply the first ratio to
        mode               (Enum) which indicates the mode applied
        ================== ===========================================================================
        **Returns**
        array              if mode is realImagniary returns a complex array, if mode is magnitudePhase
                           returns a float array
        ================== ===========================================================================
        """
        if mode == Modes.magnitudePhase :
            return self.__mixPhaseMagnitude(w1, w2, img1, img2)
        elif mode == Modes.realImaginary :
            return self.__mixRealImg(w1, w2, img1, img2)
        else:
            print("error with the mode")
    def deleteImage(self, img: int):
        """
        Responsible for deleting certain image from lists
        ================== ===========================================================================
        **Parameters**
        img                an integer indicating which image to be deleted
        ================== ===========================================================================
        """
        try:
            for value in self.__dict__.values():
                value.pop(img)
        except IndexError:
            print("This index is not added")
            pass

    def clear(self):
        """
        Responsible for clearing all class lists
        """
        try:
            for key in self.__dict__.keys():
                self.__dict__[key] = []
        except ImportError:
            print("There are no images added to be deleted")
            pass

    def __mixRealImg(self, R: float, I:float, img1: int, img2: int) -> np.ndarray:
        """
        ** Read mixer Documentation
        Mode Real/ Imaginary mix.
        Implements the following mix:
        mix = (R * realComponent1 + (1-R) * realComponent2) + j * (I * imaginaryComponent1 + (1-I) * imaginaryComponent2)
        """
        real = R * self.realComponents[img1] + (1-R)*self.realComponents[img2]
        imaginary = I * self.imaginaryComponents[img2] + (1-I)*self.imaginaryComponents[img2]
        return real + 1j * imaginary


    def __mixPhaseMagnitude(self, M: float, P:float, img1:int, img2:int) -> np.ndarray:
        """
        ** Read mixer Documentation
        Mode Phase/ Magnitude mix.
        Implements the following mix:
        mix = (M * magnitude1 + (1-M) * magnitude2) * exp (P * phase1 + (1-P) * phase2)
        """
        magnitude = M * self.imagesMagnitude[img1] + (1-M) * self.imagesMagnitude[img2]
        exponentPower = P * self.imagesPhase[img2] + (1-P) * self.imagesPhase[img2]
        return magnitude * np.exp(1j * exponentPower)

    def __addImage(self, instance, shifted: bool = False):
        """
        ** Read addImage Documentation
        Called by addImage which extracts all images components and add the in place
        """
        instance.fourierTransform(shifted)
        self.imagesTransformed.append(instance)
        self.imagesMagnitude.append(instance.magnitude())
        self.imagesPhase.append(instance.phase())
        self.realComponents.append(instance.realComponent())
        self.imaginaryComponents.append(instance.imaginaryComponent())



if __name__ == '__main__':
    img1 = image()
    img1.loadImage("TestImages/tree-736877_640.jpg")

    img1.fourierTransform()

    img2 = image()
    img2.loadImage("TestImages/landscape-4938188_640.jpg")
    img2.fourierTransform()


    mixer = mixer2Image()
    mixer.addImage([img1, img2])
    mixer.deleteImage(1)

    # output1 = mixer.mixer(0.6, 0.8,0, Modes.magnitudePhase)
    # print(output1[:1])
    # print(output1.shape)




