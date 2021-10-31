# ------ Testing code --------

import cv2
import image
import analyze
import numpy as np

frame = cv2.imread("pride_flag.png")
# newframe = frame[0:200, 0:10]

cv2.imshow("test", frame)




clim = (380, 750)
# for row in newframe:
#     print(row)
normFrame = analyze.normalizeRGB(frame)

wavelengths = np.arange(clim[0],clim[1]+1,2)
tally = dict(zip(wavelengths, np.zeros(len(wavelengths))))
wlRGB = np.array((analyze.wavelength_to_rgb(wl) for wl in wavelengths))


cv2.waitKey(0)