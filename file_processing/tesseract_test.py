from pdf2image import convert_from_path
from PIL import Image
import pytesseract

try:
    print(pytesseract.get_tesseract_version())
except pytesseract.TesseractNotFoundError:
    print("Tesseract is not installed or not found in PATH. Follow https://tesseract-ocr.github.io/tessdoc/Installation.html")

class read_tesseract:
    """
    OCR usign Tesseract

    extract_image(image_path) <- function
    
    extract_pdf(pdf_path) <- function
    """

    def extract_image(image_path):
        """
        Text Extraction from Image

        image_path : Path of image file
        """
        # Open an image file
        img = Image.open(image_path)

        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img)

        return text

    def extract_pdf(pdf_path):
        """
        Text Extraction from PDF File

        pdf_path : Path of pdf file
        """
        #list of extracted data
        page_extractions = []

        # returns the list of images i.e each page of the pdf
        images = convert_from_path(pdf_path)

        for image in images:
            text = pytesseract.image_to_string(image)
            page_extractions.append(text)

        return page_extractions

