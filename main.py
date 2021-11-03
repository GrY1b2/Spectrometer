# ------ Testing code --------

import cv2
import image
import analyze
import numpy as np

frame = cv2.imread("pride_flag.png")
frame = frame[0:200, 0:10]

cv2.imshow("test", frame)


clim = (380, 750)


wavelengths = np.arange(clim[0],clim[1]+1,1)
tally = dict(zip(wavelengths, np.zeros(len(wavelengths), dtype="int")))
wlRGB = np.array([analyze.wavelength_to_rgb(wl) for wl in wavelengths])
wlRGB *= 255.0
norm_wlRGB = wlRGB.astype("int")













cv2.waitKey(0)