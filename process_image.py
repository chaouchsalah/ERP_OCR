from PIL import Image
import os
import subprocess
import cv2

file = "CDI.png"
# Resize file dpi
im = Image.open(file)
im.save(file, dpi=(300,300))

# Binarisation of image
img = cv2.imread(file)
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imshow('dst_rt', img_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()