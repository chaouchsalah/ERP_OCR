import cv2
from PIL import Image
import subprocess
import tempfile
import numpy as np

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

image_name = 'test2.jpg'
im = Image.open(image_name)
im.save(image_name, dpi=(300,300))
image = cv2.imread(image_name)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
_,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) # threshold
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))

j=0
max = 0
max_iter = 0
while j<=15:
    dilated = cv2.dilate(thresh,kernel,iterations = j) # dilate
    _, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
    accepted=0
    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)
        # discard areas that are too large
        if h>300 and w>300:
            continue

        # discard areas that are too small
        if h<40 or w<40:
            continue
        accepted += 1
        crop_img = image[y:y+h, x:x+w]
    if accepted>max:
        max = accepted
        max_iter = j
    j+=1
    # write original image with added contours to disk  
    # cv2.imwrite("contoured.jpg", image)
dilated = cv2.dilate(thresh,kernel,iterations = max_iter)
cv2.imwrite('dilated.png',dilated)
_, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
i=0
# for each contour found, draw a rectangle around it on original image
for contour in contours:
    # get rectangle bounding contour
    [x,y,w,h] = cv2.boundingRect(contour)
    # discard areas that are too large
    if h>300 and w>300:
        continue

    # discard areas that are too small
    if h<40 or w<40:
        continue
    crop_img = image[y:y+h, x:x+w]
    filename = 'cropped/'+str(i)+'.png'
    cv2.imwrite(filename,crop_img)
    i += 1