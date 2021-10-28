# ------ Create Specrometer graph from image data -------


import cv2
import matplotlib
import image
import time
from threading import Thread

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
    while True:
        if video.getImage() is not None:
            print(video.getImage().shape)
        time.sleep(1)