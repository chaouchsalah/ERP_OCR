import tempfile
import cv2
import numpy as np
from PIL import Image
from skew import skew


IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

def process_image_for_ocr(file_path,blur_value,kernel_value,inverse=False):
    filename = file_path.split('.')
    if filename[len(filename)-1]=='png':
        im = Image.open(file_path)
        im = im.convert('RGB')
        filename[len(filename)-1]='jpg'
        file_path = '.'.join(filename)
        im.save(file_path)
    temp_filename = set_image_dpi(file_path)
    if inverse:
        im_new = remove_noise(temp_filename,blur_value)
    else:
        im_new = remove_noise_and_smooth(temp_filename,blur_value,kernel_value)
    return im_new

def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename


def image_smoothening(img,blur_value):
    _, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    _, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, blur_value, 0)
    _, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise(file_name,blur_value):
    img = cv2.imread(file_name, 0)
    img = image_smoothening(img,blur_value)
    not_image = cv2.bitwise_not(img)
    return not_image

def remove_noise_and_smooth(file_name,blur_value,kernel_value):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones(kernel_value, np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img,blur_value)
    or_image = cv2.bitwise_or(img, closing)
    return or_image

def run(image,inverse=False,resize=False):
    blur_value = (1,1)
    kernel_value = (1,1)
    image_name = image.split('.')
    if len(image_name)==2:
        image_name = image_name[0]
    else:
        image_name = ''.join(image_name[0:len(image_name)-2])
    #print('Pre-processing image : '+image_name)
    filename = image_name+'-processed.png'
    if resize:
        kernel_value = (5,5)
        blur_value = (3,3)
    image = process_image_for_ocr(image,blur_value,kernel_value,inverse)
    if resize:
        image = cv2.resize(image, (0,0), fx=1.5, fy=1.5)
    cv2.imwrite(filename,image)
    im = Image.open(filename)
    im.save(filename, dpi=(300,300))
    #print('Pre-processing finished')