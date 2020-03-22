# This is the file which contains the image class
import cv2 as cv
import numpy as np

class image():
    def __init__(self):
        self.imageData = None
        self.imageFourier = None
        self.imageFourierInv = None
        self.dataType = None
        self.imageShape = None

    def loadImage(self, path: str):
        """
        loads the specified image from its path and normalize it
        :return: image data array of a gray scale image
        """
        self.imageData = cv.imread(path)
        self.imageData = cv.cvtColor(self.imageData, cv.COLOR_RGB2GRAY)/255.0
        self.dataType = self.imageData.dtype
        self.imageShape = self.imageData.shape
        print("the image shape is ", self.imageShape)

    def clear(self):
        """
        clear all data in image object
        :return:
        """
        self.__init__()

    def fourierTransform(self):
        self.imageFourier = cv.dft(self.imageData)

    def inverseFourier(self):
        self.imageFourierInv = cv.idft(self.imageFourier)

    def realComponent(self):
        return np.real(self.imageFourier)

    def imaginaryComponent(self):
        return np.imag(self.imageFourier)

    def magnitude(self):
            return np.abs(self.imageFourier)

    def phase(self):
        return np.angle(self.imageFourier)


class mixer2Image():
    def __init__(self):
        self.imagesTransformed = []
        self.realComponents = []
        self.imaginaryComponents = []
        self.imagesPhase = []
        self.imagesMagnitude = []

    def addImage(self, image: image):
        self.imagesTransformed.append(image)

        self.imagesMagnitude.append(image.magnitude())
        self.imagesPhase.append(image.phase())
        self.realComponents.append(image.realComponent())
        self.imaginaryComponents.append(image.imaginaryComponent())

    def mixRealImg(self, R: float, I:float, img: int) -> complex:
        real = R * self.realComponents[img] + (1-R)*self.realComponents[~img]
        # print(real)
        imaginary = I * self.imaginaryComponents[img] + (1-I)*self.imaginaryComponents[~img]
        # print(imaginary)
        return np.complex(real, imaginary)

    def mixPhaseMagnitude(self):
        pass



if __name__ == '__main__':
    img1 = image()
    img1.loadImage("TestImages/tree-736877_640.jpg")
    img1.fourierTransform()

    img2 = image()
    img2.loadImage("TestImages/landscape-4938188_640.jpg")
    img2.fourierTransform()
    #
    # mixer = mixer2Image()
    #
    # mixer.addImage(img1)
    # mixer.addImage(img2)
    #
    # output1 = mixer.mixRealImg(0.6,0.8, 0)
    img1.clear()

    # print(output1)




