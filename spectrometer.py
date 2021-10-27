# ------ Create Specrometer graph from image data -------


import cv2
import numpy 
import matplotlib
import image
import time


class videoROI():
    def __init__(self, videoObj):
        self.capture = videoObj
        self.bbox = None        # In format (pos1, pos2)v: Tuple[Tuple, Tuple]
    
    def show(self):
        cv2.imshow("image", self.capture)


if __name__ == "__main__":
    this = videoROI(cv2.videoCapture(0))
    this.update()