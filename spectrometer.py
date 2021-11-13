# ------ Create Specrometer graph from image data -------

# Creates a video feed of the camera, lets the user select an ROI and graph the data
# Sometimes the script crashes randomly. Just restart. Little time has been dedicated to user interface and EoA. 
# This spectrometer is by no means perfect, but is working surprisingly well. 

import cv2
import matplotlib.pyplot as plt
import image
import numpy as np
from threading import Thread
import time

# Class to keep a static ROI over video
class videoROI(Thread):
    def __init__(self, src, topleft, bottomright):
        super().__init__()
        self.bbox = [topleft, bottomright]        # Bounding box for rectangle, (topleft, bottomright)
        self.windowName = "Video"
        self._frame = None
        self.src = src
        self.scale = 2                            # Scale to increase the image resolution of when displaying
    
    def run(self, *args, **kwargs):
        """
        Main function of thread
        """
        self.capture = cv2.VideoCapture(self.src)       # src = 0: built in webcam, src = 1: additional webcam

        cv2.namedWindow(self.windowName)

        while self.capture.isOpened():

            # Capture image for video feed 
            self._frame = image.getImage(self.capture, *self.bbox)

            # Sometimes async errors causes frame to be None
            if self._frame is None:
                cv2.waitKey(1)
                continue
            
            # Increase the resolution/size of the shown video feed to fit laptop display better
            show_frame = cv2.resize(self._frame, (640*self.scale, 480*self.scale))
            cv2.imshow(self.windowName, show_frame)
            
            k = cv2.waitKey(1)

            # User input
            # 'p': print the coordinates of the mouse
            # 'q': quit
            # 's': save current image
            if k == ord('p'):
                cv2.setMouseCallback(self.windowName, self.mouseCB, param=0)
            elif k == ord('q'):
                break
            elif k == ord('s'):
                cv2.imwrite("frame.png", self._frame)
        else:
            print("capture closed")

    def mouseCB(self, event, x, y, flags, param):
        """
        Mouse event callback
        Print the coordinates of the mouse once.
        """
        print("Pos: {}, {}".format(x/self.scale,y/self.scale))

        # Set next callback to anonymous function returning None
        cv2.setMouseCallback(self.windowName, lambda *args : None)

    def getImage(self):
        """
        Get current ROI
        """
        return image.getSubImage(self.capture, *self.bbox)

    def close(self):
        """
        Close the camera
        """
        image.closeCamera(self.capture)
        

if __name__ == "__main__":
    
    # Analyze 2 lines of spectrum at height 300. 
    pixelY = 300
    height = 2

    # Calibration constants
    calibWL = 532       # Calibrated to prefectly match green laser
    calibPixelX = 189   # Green laser x value on detector
    minWL = 300         # Minimum wavelength to be graphed
    maxWL = 800         # Max wavelength to be graphed
    scaleFactor = 2.6   # Calculated resolution (wavelengths per pixel) with other known lasers with green laser being zero

    # Arange wavelength array
    calibToMax = np.arange(calibWL, maxWL, scaleFactor)
    calibToMin = np.flip(np.arange(calibWL, minWL, -scaleFactor))
    wavelengths = np.concatenate((calibToMin, calibToMax))

    # Determine the x interval of interest in detector
    minPixelX = calibPixelX - len(calibToMin) + 1
    maxPixelX = minPixelX + len(wavelengths)

    # Dictionary to count intensity of each pixel/corresponding wavelength
    intensities = dict(zip(wavelengths, np.zeros(len(wavelengths), dtype="int")))

    # Graph to plot the wavelengths on the x-axis and intensity of pixel/wavelength on the y-axis. 
    # Pixels can have a max intensity of 585000 given by square of the sum of 8-bit color value. 
    graph = plt.plot(intensities.keys(), intensities.values(), color='darkred')[0]
    plt.ylim(0, 600000)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.ion()

    # Start video feed
    video = videoROI(1, (minPixelX, pixelY), (maxPixelX, pixelY + height))
    video.start()
    time.sleep(1)

    # Main loop
    while True:

        # Analyze current image
        frame = video.getImage()

        # Close the program if the video feed is quit/closed
        if not video.is_alive():
            plt.close()
            break

        # Sometimes async errors causes frame to be None
        if not frame is None:

            # Iterate through every pixel of image with index, the index corresponds to it's approximate corresponding wavelength
            for row in frame:
                for colN, col in enumerate(row):

                    # The intensity of the pixel is calculated by the square of the sum of the pixel's 8-bit color value
                    # The square is simply to eliminate significantly less bright pixels, which are often times just noise 
                    intensities[wavelengths[colN]] += np.sum(col) * np.sum(col)

            # If more than one row of pixels are analyzed, average the intensity values. 
            if height != 1:
                for k, v in intensities.items():
                    intensities[k] = v/height
            
            # Plot the data
            yData = list(intensities.values())
            graph.set_ydata(yData)
            plt.pause(0.1)

            # Reset the intensities between each frame
            intensities = dict(zip(wavelengths, np.zeros(len(wavelengths), dtype="int")))