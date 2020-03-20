# This is the file which contains the image class
import cv2 as cv


class image():
    """
    this class is the maintaining class for all actions done on an image
    """
    def __init__(self):
        self.imageData = None
        self.imageFourier = None



    def loadImage(self, path):
        """
        loads the specified image from its path
        :return: image data array
        """
        self.imageData = cv.imread(path)

    def fourierTransform(self):
        self.imageFourier = cv.dft(self.imageData)


if __name__ == '__main__':
    img = image()
    img.loadImage("TestImages/cat-1792684_640.jpg")
    print(img.imageData)
    img.fourierTransform()
    print(img.imageFourier)




