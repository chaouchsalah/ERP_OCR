import pyzbar.pyzbar as pyzbar
import cv2
 
def decode(image) :
    im = cv2.imread(image)
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
        return str(obj.data).split('\'')[1]
    return None