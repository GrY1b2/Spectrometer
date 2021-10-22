# ------ Testing code --------

import image
import cv2


frame = image.getImage((20,30),(200,400))

cv2.imshow("test", frame)

k=cv2.waitKey(0)
