import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import Barcode.BarcodeReader as BarcodeReader
import tempfile

def BarcodeScanner(image_binary):
    # Load the image data into a NumPy array
    image = np.frombuffer(image_binary, dtype=np.uint8)
    # Decode the image data into a OpenCV image
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect barcodes in the image
    barcodes = pyzbar.decode(gray)

    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # The barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcode_data = barcode.data.decode("utf-8")
        return BarcodeReader.BarcodeReaderFunc(barcode_data)