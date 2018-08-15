import subprocess
import os

language = 'fra'
keyword_whitelist = 'tessedit_char_whitelist='
whitelist = keyword_whitelist + 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ°1234567890|%/()$€,.:+-\'# '
def run(image,facture=False):
    psm = '6'
    if facture:
        psm = '7'
    image_name = image.split('.')
    if len(image_name)==2:
        image = image_name[0]
    else:
        image = image_name[0:len(image_name)-2]
    filename = image+'-processed.png'
    #print('OCR step begins for image : '+image)
    output_file = image
    comm=['tesseract',filename,output_file,
        '-l',language,
        '-c',whitelist,
        '-c','preserve_interword_spaces=1',
        '-psm',psm]
    subprocess.run(comm, shell=True)
    os.remove(filename)
    #print('OCR step finishes')