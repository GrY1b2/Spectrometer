# ------- Capture and return image --------

import cv2

CAM = cv2.VideoCapture(0)

def getImage(p1=None, p2=None):
    """
    Returns the image with drawn rectangle on top given by pt1 and pt2
    """
    ret, frame = CAM.read()
    if not ret:
        print("failed to grab frame")
        return None
    
    if p1 and p2:
        cv2.rectangle(frame, p1, p2, (255,0,0))
    
    return frame

def getSubImage(p1, p2):
    """"
    Returns the part of the capture enclosed by pt1 and pt2.
    """

    frame = getImage()
    analyze_frame = frame[p1[1]:p2[1], p1[0]:p2[0]]

    return analyze_frame




def closeCamera():
    CAM.release()
    cv2.destroyAllWindows()

