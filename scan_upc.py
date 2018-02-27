from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2


def decode(im):
    # Find barcodes
    decodedObjects = pyzbar.decode(im)

    # Print results
    for obj in decodedObjects:
        print('Barcode : ', obj.data)

    return decodedObjects

# Main
if __name__ == '__main__':

    # Read image (change test.jpg to appropriate image name/extension to test
    im = cv2.imread('test.jpg')
    decodedObjects = decode(im)
