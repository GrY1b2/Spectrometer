# ------ Testing code --------

import cv2
import image
import analyze

video = cv2.VideoCapture(0)


frame = image.getSubImage(video, (100,100), (120,120))
frame2 = image.getImage(video)

cv2.imshow("test", frame)
cv2.imshow("window", frame2)
#analyze.getImageColor(frame)

cv2.waitKey(0)

for wl in range(200, 1000):
    print(wl, analyze.wavelength_to_rgb(wl))