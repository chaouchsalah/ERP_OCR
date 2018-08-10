import cv2
import subprocess
from PIL import Image
import numpy as np

im = Image.open('Facture.jpg')
im.save('Facture.jpg', dpi=(300,300))
img = cv2.imread('Facture.jpg',0)
ret3,th3 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,-2)
"""
vertical = th2.copy()
vertical_size = vertical.shape[0]//50
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,vertical_size))
vertical = cv2.erode(vertical,kernel,iterations = 1)
vertical = cv2.dilate(vertical,kernel,iterations = 1)
mask = vertical
cv2.imwrite('mask.png',mask)
no_border = np.bitwise_or(mask,th3)"""
cv2.imwrite('final.png',th3)
im = Image.open('final.png')
im.save('final.png', dpi=(300,300))

filename = "final.png"
output_file = "OUTfinal"
language = "fra"
comm=["tesseract",filename,output_file,"-l",language,"-psm","6"]
subprocess.run(comm, shell=True)