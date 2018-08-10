import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import subprocess

im = Image.open('Facture.jpg')
im.save('Facture.jpg', dpi=(300,300))
img = cv2.imread('Facture.jpg',0)
"""
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)"""
ret3,th3 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imwrite('gauss.png',th3)

# Resize file dpi
im = Image.open('gauss.png')
im.save('gauss.png', dpi=(300,300))

filename = "gauss.png"
output_file = "outputbase"
language = "fra"
comm=["tesseract",filename,output_file,"-l",language,"-psm","6"]
subprocess.run(comm, shell=True)
