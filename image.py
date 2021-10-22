# ------- Capture and return image --------

import cv2

CAM = cv2.VideoCapture(0)

def getImage(pt1=None, pt2=None):
    """
    Returns the image with drawn rectangle on top given by pt1 and pt2
    """
    ret, frame = CAM.read()
    if not ret:
        print("failed to grab frame")
        return None
    if pt1 and pt2:
        cv2.rectangle(frame, pt1, pt2, (255,0,0))
    
    return frame

def getSubImage(pt1, pt2):
    """"
    Returns the part of the capture enclosed by pt1 and pt2
    """

    frame = getImage()
    analyze_frame = frame[slice(analyze_bbox[0][1], analyze_bbox[1][1]), slice(analyze_bbox[0][0], analyze_bbox[1][0])]

    return frame




def closeCamera():
    CAM.release()
    cv2.destroyAllWindows()

