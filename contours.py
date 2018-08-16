import cv2
from PIL import Image
import subprocess
import tempfile
import numpy as np

cropped = []

# Check if image is close enough to be a replicate
def between(val1,val2):
    if val2 <= val1+10 and val2 >= val1-10:
        return True
    return False

# Check if image is a replicate
def exist(arr):
    for crop in cropped:
        if between(crop[0],arr[0]) and between(crop[1],arr[1]):
            return True
    return False

def run(image_name):
    global cropped
    cropped = []
    image = cv2.imread(image_name)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))

    j=0
    i=0
    while j<=15:
        dilated = cv2.dilate(thresh,kernel,iterations = j)
        # Extract contours from image
        _,contours,_ = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        
        # For each contour found extract the rectangle bounding it
        for contour in contours:
            # Extract the rectangle bounding contours
            [x,y,w,h] = cv2.boundingRect(contour)
            # Ignore small and large images
            if (h>500 and w>400) or w<1300 or (w<400 and h<400):
                continue
            # Check for replicate
            if not exist([x,y,w,h]):
                cropped.append([x,y,w,h])
                crop_img = image[y:y+h, x:x+w]
                filename = 'cropped/'+str(i)+'.jpg'
                cv2.imwrite(filename,crop_img)
                im = Image.open(filename)
                im.save(filename, dpi=(300,300))
                i+=1
        j+=1