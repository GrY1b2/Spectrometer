# ------ Create Specrometer graph from image data -------

import cv2
import matplotlib.pyplot as plt
import matplotlib.colors
import image
import time
import numpy as np
from threading import Thread
import analyze

# Class to keep a static ROI over video
class videoROI(Thread):
    def __init__(self, src):
        super().__init__()
        self.bbox = [None, None]        # In format [pos1, pos2] : List[Tuple, Tuple]
        self.windowName = "image"
        self.frame = None
        self.src = src
    
    @property
    def selected(self):
        return all(self.bbox)
    
    def run(self, *args, **kwargs):

        self.capture = cv2.VideoCapture(self.src)
        self.capture.set(3, 64)
        self.capture.set(4, 64)
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)

        while self.capture.isOpened():

            self.frame = image.getImage(self.capture, *self.bbox)

            
            cv2.imshow(self.windowName, self.frame)
            k = cv2.waitKey(1)

            if k == ord('c'):     # Draw rectangle
                self.bbox = [None, None]
                cv2.setMouseCallback(self.windowName, self.mouseCB, param=0)
                while not all(self.bbox):
                    k = cv2.waitKey(1)

            elif k == ord('q'):
                break

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
            if all(self.bbox):
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

    # norm = plt.Normalize(*clim)
    # colorlist = list(zip(norm(wavelengths),[analyze.wavelength_to_rgb(w) for w in wavelengths]))
    # spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)
    # fig, axs = plt.subplots(1, 1, figsize=(8,4), tight_layout=True)
    graph = plt.plot(tally.keys(), tally.values(), color='darkred')[0]
    plt.ylim(0, 50)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.ion()

    video = videoROI(0)
    video.start()

    while True:

        if video.selected: 
            frame = video.getImage()

            newframe = np.reshape(frame, (frame.shape[0] * frame.shape[1], 3))
            for col in newframe:
                if all(np.flip(col) < np.array([30,30,30])) or all(np.flip(col) > np.array([100,100,100])):
                    continue
                prevdiff = (10000000, 0)
                for i, wlCol in enumerate(norm_wlRGB):
                    diff = np.linalg.norm(np.flip(col)-wlCol[:-1])
                    if diff < prevdiff[0]:
                        prevdiff = (diff, i)
                tally[wavelengths[prevdiff[1]]] += 1

            graph.set_ydata(list(tally.values()))
            plt.draw()
            plt.pause(0.1)
            tally = dict.fromkeys(tally, 0)
        cv2.waitKey(10)




    # clim=(380,750)
    
    # wl = np.arange(clim[0],clim[1]+1,2)

    
    
    
    # # Mainloop
    # i = 0
    # while True:
    #     i += 1
    #     print("in here")
    #     spectrum = (np.sin(wavelengths*i/100) +5)
    #     if i == 100:
    #         i = 0
    #     plt.clf()
    #     plt.imshow(X, clim=clim,  extent=extent, cmap=spectralmap, aspect='auto')
    #     plt.fill_between(wavelengths, spectrum, 8, color='w')
    #     graph.set_ydata(spectrum)
    #     plt.draw()
    #     plt.pause(0.1)

