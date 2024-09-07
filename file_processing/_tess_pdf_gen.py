from pdf2image import convert_from_path
# from PIL import Image
import pytesseract
try:
    print(pytesseract.get_tesseract_version())
except pytesseract.TesseractNotFoundError:
   print("Tesseract is not installed or not found in PATH. Follow https://tesseract-ocr.github.io/tessdoc/Installation.html")

from PIL import Image
from fpdf import FPDF

#handling structured format
# custom_config = r'--psm 6'  # or other modes based on the document type
images = convert_from_path("test.pdf")

# Open an image file
img = Image.open('test.png')

text = pytesseract.image_to_string(images[0])#,config=custom_config)

# Writing the resutls to a pdf
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

for line in text.splitlines():
    pdf.cell(200, 10, txt=line, ln=True, align='L')

pdf_output_path = "tess_generated_test.pdf"
pdf.output(pdf_output_path)

print(f"PDF generated successfully: {pdf_output_path}")