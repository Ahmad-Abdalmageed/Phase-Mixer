## This is the abstract class that the students should implement

from modesEnum import Modes
import numpy as np
import image

class ImageModel():

    """
    A class that represents the ImageModel
    """
    def __init__(self, imgPath: str):
        self.imgPath = imgPath
        ###
        # ALL the following properties should be assigned correctly after reading imgPath
        ###
        self.mixer = image.mixer2Image()
        self.path = imgPath

        self.imgByte = None
        self.dft = None
        self.real = None
        self.imaginary = None
        self.magnitude = None
        self.phase = None
        self.setting()
        print(self.__dict__.values())


    def setting(self) -> image.image:
        """
        This function is responsible for loading the image.image class into the class
        ================== ===========================================================================
        ** Returns**
        image              an instance from image.image
        ================== ===========================================================================
        """
        # initializing the image
        self.image = image.image()
        self.image.loadImage(path=self.path)
        self.mixer.addImage(self.image)

        # Assigning the attributes
        self.imgByte = self.image.imageData
        self.dft = self.image.imageFourier
        self.real = np.copy(self.image.realComponent())
        self.imaginary = np.copy(self.image.imaginaryComponent())
        self.magnitude = np.copy(self.image.magnitude())
        self.phase = np.copy(self.image.phase())

        return self.image

    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        """
        a function that takes ImageModel object mag ratio, phase ration and
        return the magnitude of ifft of the mix
        return type ---> 2D numpy array

        please Add whatever functions realted to the image data in this file
        """
        ###
        # implement this function
        ###
        self.mixer.addImage(imageToBeMixed.setting())
        return self.mixer.mix(magnitudeOrRealRatio, phaesOrImaginaryRatio, 0, 1, mode)
