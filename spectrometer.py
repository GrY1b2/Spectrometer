# ------ Create Specrometer graph from image data -------

# Creates a video feed of the camera, lets the user select an ROI and graph the data
# Sometimes the script crashes randomly. Just restart. Little time has been dedicated to user interface and EoA. 
# This spectrometer is by no means perfect, but is working surprisingly well. 

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
        self.bbox = [None, None]        # Bounding box for rectangle, (topleft, bottomright)
        self.windowName = "image"
        self.frame = None
        self.src = src
    
    @property
    def selected(self):
        return all(self.bbox)
    
    def run(self, *args, **kwargs):
        """
        Main function of thread
        """
        self.capture = cv2.VideoCapture(self.src)       # src = 0: built in webcam, src = 1: additional webcam

        # Set a lower resolution to quicken computation.
        self.capture.set(3, 256)
        self.capture.set(4, 256)

        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)

        while self.capture.isOpened():

            # Show a video feed of the camera
            self.frame = image.getImage(self.capture, *self.bbox)
            cv2.imshow(self.windowName, self.frame)
            k = cv2.waitKey(1)

            # User input
            # 'c': Select an ROI
            # 'q': quit
            # 's': save current image
            if k == ord('c'):
                self.bbox = [None, None]

                # Wait until both positions are selected until continuing the video feed.
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
        """
        Mouse event callback
        param is an integer representing the bounding box position index
        """
        if param == 0 and event == cv2.EVENT_LBUTTONDOWN:
            # First bbox index
            self.bbox[param] = (x,y)
            cv2.setMouseCallback(self.windowName, self.mouseCB, param=1)
        elif param == 1 and event == cv2.EVENT_LBUTTONDOWN:
            # Second bbox index, disregard next mouse event by setting callback to an anonymous function
            self.bbox[param] = (x,y)
            cv2.setMouseCallback(self.windowName, lambda *args : None)
        elif param == 1:
            # Live update ROI rectangle
            newframe = self.frame.copy()
            cv2.rectangle(newframe, self.bbox[0], (x,y), (0,255,0))
            cv2.imshow("image", newframe)

    def getImage(self):
        """
        Get current image (or ROI if selected)
        """
        try:
            if self.selected:
                return image.getSubImage(self.capture, *self.bbox)
            else:
                return image.getImage(self.capture, *self.bbox)
        except AttributeError:
            return None
        

if __name__ == "__main__":
    # Visible color (lower, upper) limit
    clim = (380, 750)

    # Arrange wavelength array
    wavelengths = np.arange(clim[0],clim[1]+1,3)

    # Dictionary to count pixels with the wavelength as the key
    tally = dict(zip(wavelengths, np.zeros(len(wavelengths), dtype="int")))

    # Wavelength array in RGB-value, normalized to a value between 0 and 255
    wlRGB = np.array([analyze.wavelength_to_rgb(wl) for wl in wavelengths])
    wlRGB *= 255.0
    norm_wlRGB = wlRGB.astype("int")

    # Plot to plot the wavelengths on the x-axis and # of pixels on the y axis. the number of pixels of each wavelengths will represent the intensity.
    graph = plt.plot(tally.keys(), tally.values(), color='darkred')[0]
    plt.ylim(0, 50)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.ion()

    # Start video feed
    video = videoROI(1)
    video.start()

    # main loop
    while True:
        if video.selected: 

            # Get current frame and iterate through every pixel
            frame = video.getImage()
            for row in frame:
                for col in row:

                    # Pixel return value in (B, G, R, A), Alpha value will not be used and the rest are flipped to get (R, G, B) value
                    flip = np.flip(col)

                    # If the pixel is very dim or includes lots of light of all colors, ignore it
                    if all(flip < np.array([50,50,50])) or all(flip > np.array([100,100,100])):
                        continue

                    # Iterate through every wavelength (R, G, B) value
                    # Calculate the difference in magnitude between the wavelength and the pixel vector
                    # The lowest difference value will correspond to the closest matching wavelength of pixel
                    # Add 1 to the pixel counter corresponding to the wavelength 
                    prevdiff = (10000000, 0)
                    for i, wlCol in enumerate(norm_wlRGB):
                        diff = np.sum(np.square(flip - wlCol[:-1]))     # magnitude of color vector without sqrt() operation.
                        if diff < prevdiff[0]:
                            prevdiff = (diff, i)
                    try:
                        tally[wavelengths[prevdiff[1]]] += 1
                    except:
                        pass

            # Remove extremes. This will mostly contain noise
            tally[wavelengths[0]] = 0
            tally[wavelengths[-1]] = 0

            # Graph the data
            yData = list(tally.values())
            graph.set_ydata(yData)
            plt.ylim(0, max(yData) + 2)
            plt.draw()
            plt.pause(0.01)
            cv2.waitKey(1)

            tally = dict.fromkeys(tally, 0)
        