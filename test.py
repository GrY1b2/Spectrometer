# ------ Testing code --------

import cv2
import image
import analyze
import numpy as np

for wl in range(1000):
    print(wl ,analyze.wavelength_to_rgb(wl))
