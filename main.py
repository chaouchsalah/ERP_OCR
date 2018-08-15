import preprocessing
import processing
import postprocessing
import extraction
import contours
from os import listdir
import os
from multiprocessing.dummy import Pool as ThreadPool
import glob

images = []
for i in range(4,5):
    filename = 'test'+str(i)+'.jpg'
    images.append(filename)

# If true inverse the binarisation of the image
def is_inverse(extracted_data):
    e = extracted_data
    return 'if' not in e or 'cnss' not in e or 'patente' not in e or 'rc' not in e

def extract(filename,inverse=False,resize=False,facture=False):
    preprocessing.run(filename,inverse,resize,facture)
    processing.run(filename,facture)
    postprocessing.run(filename)
    return extraction.run(filename)

# Combine 2 extracted data objects into 1
def combine_extracted(extracted_data1,extracted_data2):
    cases = ['if','cnss','patente','rc']
    for data in extracted_data2:
        if data not in extracted_data1 or data in cases:
            extracted_data1[data] = extracted_data2[data]
    return extracted_data1

def process(filename):
    extracted_data = extract(filename)
    if 'facture' not in extracted_data:
        extracted_data2 = extract(filename,False,False,True)
        extracted_data = combine_extracted(extracted_data,extracted_data2)
    # If facture not found
    if 'facture' not in extracted_data:
        # Split image into multiple parts
        contours.run(filename)
        # The path for the extracted images
        file_path = 'cropped'
        images = listdir(file_path)
        for image in images:
            if '.jpg' in image:
                extracted_data2 = extract(file_path+'/'+image,False,True,False)
                extracted_data = combine_extracted(extracted_data,extracted_data2)
                os.remove(file_path+'/'+image)
    if is_inverse(extracted_data):
        extracted_data2 = extract(filename,True,False,False)
        extracted_data = combine_extracted(extracted_data,extracted_data2)
    for data in extracted_data:
        extracted_data[data] = extracted_data[data].replace('\n',' ').strip()
    return extracted_data

def run(images):
    results = []
    for image in images:
        results.append(process(image))
    return results

"""def run():
    results = []
    for image in images:
        results.append(process(image))
    print(results)
run()"""