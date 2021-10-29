# ------ Testing code --------

import cv2
import image
import analyze

frame = cv2.imread("pride_flag.png")
# newframe = frame[0:200, 0:10]

cv2.imshow("test", frame)



cv2.waitKey(0)
print(frame[5,5])
clim = (380, 750)
# for row in newframe:
#     print(row)
newframe = analyze.normalizePixelColor(frame, clim)

print(frame[5,5])
# for row in newframe:
#     print(newframe)