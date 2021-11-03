# ------ Create Specrometer graph from image data -------

import cv2
import matplotlib.pyplot as plt
import image
import numpy as np
from threading import Thread
import analyze

# Class to keep a static ROI over video
class videoROI(Thread):
    def __init__(self, src):
        super().__init__()
        self.bbox = [None, None]
        self.windowName = "image"
        self.frame = None
        self.src = src
    
    @property
    def selected(self):
        return all(self.bbox)
    
    def run(self, *args, **kwargs):

        self.capture = cv2.VideoCapture(self.src)
        self.capture.set(3, 128)
        self.capture.set(4, 128)
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)

        while self.capture.isOpened():

            self.frame = image.getImage(self.capture, *self.bbox)

            
            cv2.imshow(self.windowName, self.frame)
            k = cv2.waitKey(1)

            if k == ord('c'):
                self.bbox = [None, None]
                cv2.setMouseCallback(self.windowName, self.mouseCB, param=0)
                while not all(self.bbox):
                    k = cv2.waitKey(1)

            elif k == ord('q'):
                break
                
            elif k == ord('s'):
                cv2.imwrite("frame.png", self.frame)

        else:
            print("capture closed")

    def mouseCB(self, event, x, y, flags, param):

        if param == 0 and event == cv2.EVENT_LBUTTONDOWN:
            self.bbox[param] = (x,y)
            cv2.setMouseCallback(self.windowName, self.mouseCB, param=1)
        elif param == 1 and event == cv2.EVENT_LBUTTONDOWN:
            self.bbox[param] = (x,y)
            cv2.setMouseCallback(self.windowName, lambda *args : None)
        elif param == 1:
            newframe = self.frame.copy()
            cv2.rectangle(newframe, self.bbox[0], (x,y), (0,255,0))
            cv2.imshow("image", newframe)

    def getImage(self):
        try:
            if self.selected:
                return image.getSubImage(self.capture, *self.bbox)
            else:
                return image.getImage(self.capture, *self.bbox)
        except AttributeError:
            return None
        
if __name__ == "__main__":
    clim = (380, 750)

    wavelengths = np.arange(clim[0],clim[1]+1,2)
    tally = dict(zip(wavelengths, np.zeros(len(wavelengths), dtype="int")))
    wlRGB = np.array([analyze.wavelength_to_rgb(wl) for wl in wavelengths])
    wlRGB *= 255.0
    norm_wlRGB = wlRGB.astype("int")

    graph = plt.plot(tally.keys(), tally.values(), color='darkred')[0]
    plt.ylim(0, 50)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.ion()

    video = videoROI(1)
    video.start()

    while True:

        if video.selected: 
            frame = video.getImage()

            newframe = np.reshape(frame, (frame.shape[0] * frame.shape[1], 3))
            for row in frame:
                for col in row:
                    flip = np.flip(col)
                    if all(flip < np.array([50,50,50])) or all(flip > np.array([100,100,100])):
                        continue
                    prevdiff = (10000000, 0)
                    for i, wlCol in enumerate(norm_wlRGB):
                        diff = np.sum(np.square(flip - wlCol[:-1]))     # Size of color vector without sqrt() operation.
                        if diff < prevdiff[0]:
                            prevdiff = (diff, i)
                    tally[wavelengths[prevdiff[1]]] += 1

            tally[wavelengths[0]] = 0
            tally[wavelengths[-1]] = 0
            yData = list(tally.values())
            graph.set_ydata(yData)
            plt.ylim(0, max(yData) + 2)
            plt.draw()
            plt.pause(0.01)
            cv2.waitKey(1)
            tally = dict.fromkeys(tally, 0)
        