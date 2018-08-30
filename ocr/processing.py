import subprocess
import os

LANGUAGE = 'fra'
KEYWORD_WHITELIST = 'tessedit_char_whitelist='
WHITELIST = KEYWORD_WHITELIST + 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ°1234567890|%/()$€,.:+-\'# '
def run(image):
    # Extract image name
    image_name = image.split('.')
    if len(image_name)==2:
        image = image_name[0]
    else:
        image = image_name[0:len(image_name)-2]
    filename = image+'-processed.png'
    #print('OCR step begins for image : '+image)
    output_file = image
    comm=['tesseract',filename,output_file,
        '-l',LANGUAGE,
        '-c',WHITELIST,
        '-c','preserve_interword_spaces=1',
        '-psm','6']
    subprocess.run(comm, shell=True)
    os.remove(filename)
    #print('OCR step finishes')