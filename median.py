import tempfile
import cv2
import subprocess
import numpy as np
from PIL import Image
from spellchecker import SpellChecker


IMAGE_SIZE = 1800
BINARY_THREHOLD = 180
spell = SpellChecker(language='fr')


def process_image_for_ocr(file_path):
    filename = file_path.split('.')
    if filename[len(filename)-1]=='png':
        im = Image.open(file_path)
        im = im.convert('RGB')
        filename[len(filename)-1]='jpg'
        file_path = '.'.join(filename)
        im.save(file_path)
    temp_filename = set_image_dpi(file_path)
    im_new = remove_noise_and_smooth(temp_filename)
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


def image_smoothening(img):
    _, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    _, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    _, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image

language = "fra"
keyword_whitelist = "tessedit_char_whitelist="
whitelist = keyword_whitelist + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ°1234567890|%/.:-'# "
i=1
images = ['Facture.jpg','facture-achat.jpg','facture-peugeot.jpg','bon-livraison.png']
for image in images:
    print('Pre-processing image : '+image)
    filename = 'processed.png'
    cv2.imwrite(filename,process_image_for_ocr(image))
    im = Image.open(filename)
    im.save(filename, dpi=(300,300))
    print('Pre-processing finished')
    print('OCR step begins for image : '+image)
    output_file = "OUTfinal"+str(i)
    comm=["tesseract",filename,output_file,
        "-l",language,
        "-c",whitelist,
        "--user-words","fra.wordlist",
        "--user-patterns","fra.user-patterns",
        "-c","preserve_interword_spaces=1",
        "-psm","6"]
    subprocess.run(comm, shell=True)
    print('OCR step finishes')
    i+=1