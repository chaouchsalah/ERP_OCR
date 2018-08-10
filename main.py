import preprocessing
import processing
import postprocessing
import extraction
import contours
from os import listdir
from multiprocessing.dummy import Pool as ThreadPool 

images = []
for i in range(1,4):
    filename = 'test'+str(i)+'.jpg'
    images.append(filename)

# If true inverse the binarisation of the image
def is_inverse(extracted_data):
    e = extracted_data
    return 'if' not in e or 'cnss' not in e or 'patente' not in e or 'rc' not in e

def extract(filename,inverse=False,resize=False):
    preprocessing.run(filename,inverse,resize)
    processing.run(filename)
    postprocessing.run(filename)
    return extraction.run(filename)

# Combine 2 extracted data objects into 1
def combine_extracted(extracted_data1,extracted_data2):
    for data in extracted_data2:
        if data not in extracted_data1:
            extracted_data1[data] = extracted_data2[data]
    return extracted_data1

def process(filename):
    extracted_data = extract(filename)
    # If facture not found
    if 'facture' not in extracted_data:
        # Split image into multiple parts
        contours.run(filename)
        # The path for the extracted images
        file_path = 'cropped'
        images = listdir(file_path)
        for image in images:
            if '.jpg' in image:
                extracted_data2 = extract(file_path+'/'+image,False,True)
                extracted_data = combine_extracted(extracted_data,extracted_data2)
    """elif is_inverse(extracted_data):
        extracted_data2 = extract(filename,True,False)
        extracted_data = combine_extracted(extracted_data,extracted_data2)"""
    print(extracted_data)

def run():
    for image in images:
        process(image)
    """pool = ThreadPool(4) 
    pool.map(process, images)
    pool.close()
    pool.join()"""

run()