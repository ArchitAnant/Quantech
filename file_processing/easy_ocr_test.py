import easyocr
import numpy as np
import cv2
from pdf2image import convert_from_path
from PIL import Image


class read_easyocr:
    """
    OCR usign EasyOCR

    extract_image(image_path) <- function
    
    extract_pdf(pdf_path) <- function

    By default the gpu=True. Change by passing gpu while initialization.
    """

    def __init__(self,gpu=True):
        self.reader = easyocr.Reader(['en'],gpu = gpu)

    
    def extract_image(self,image_path):
        """
        Text Extraction from Image

        image_path : Path of the image
        """
        img = Image.open(image_path)
        #convert the image space
        image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        #read the results
        result = self.reader.readtext(image)
        return result
    
    def extract_pdf(self,pdf_path):
        #result list for every page extraction 
        page_extractions = []

        # get the images list
        images = convert_from_path(pdf_path)

        for image in images:
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            result = self.reader.readtext(image)
            page_extractions.append(result)
        
        return page_extractions

