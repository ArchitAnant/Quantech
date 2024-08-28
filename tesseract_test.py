from pdf2image import convert_from_path
# from PIL import Image
import pytesseract
try:
    print(pytesseract.get_tesseract_version())
except pytesseract.TesseractNotFoundError:
    print("Tesseract is not installed or not found in PATH. Follow https://tesseract-ocr.github.io/tessdoc/Installation.html")


# custom_config = r'--psm 6'  # or other modes based on the document type

#convertion requied from pdf to image
images = convert_from_path("test.pdf")


# Open an image file
# img = Image.open('test.png')

# Use Tesseract to do OCR on the image
text = pytesseract.image_to_string(images[0])#,config=custom_config)
print(text)