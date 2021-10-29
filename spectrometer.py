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
    
    def run(self, *args, **kwargs):

        self.capture = cv2.VideoCapture(self.src)
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
    video = videoROI(0)
    video.start()
    clim=(380,750)
    norm = plt.Normalize(*clim)
    wl = np.arange(clim[0],clim[1]+1,2)
    colorlist = list(zip(norm(wl),[analyze.wavelength_to_rgb(w) for w in wl]))
    spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)
    fig, axs = plt.subplots(1, 1, figsize=(8,4), tight_layout=True)
    wavelengths = np.linspace(200, 1000, 801)       # X-axis
    spectrum = (np.sin(wavelengths*0.05) +5)
    graph = plt.plot(wavelengths, spectrum, color='darkred')[0]
    y = np.linspace(0, 6, 100)
    X,Y = np.meshgrid(wavelengths, y)
    extent=(np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.savefig('WavelengthColors.png', dpi=200)
    plt.ion()
    
    
    
    # Mainloop
    i = 0
    while True:
        i += 1
        print("in here")
        spectrum = (np.sin(wavelengths*i/100) +5)
        if i == 100:
            i = 0

        
        


        plt.clf()
        plt.imshow(X, clim=clim,  extent=extent, cmap=spectralmap, aspect='auto')
        plt.fill_between(wavelengths, spectrum, 8, color='w')
        graph.set_ydata(spectrum)
        plt.draw()
        plt.pause(0.1)