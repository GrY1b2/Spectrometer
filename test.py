# ------ Testing code --------

import image
import cv2


frame = image.getImage()

cv2.imshow("test", frame)

k=cv2.waitKey(0)
