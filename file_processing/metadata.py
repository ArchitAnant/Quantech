import os
import PyPDF2
from docx import Document
import chardet
import fitz


file_path = '/Users/architanant/Documents/Quantech/file_processing/multifile.pdf'


def print_pdf(file_path):
    lines = []

# Open the PDF file
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Get the number of pages
        num_pages = len(pdf_reader.pages)
        print(f"Number of pages: {num_pages}")

        # Extract text from each page
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            print(f"Page {page_num + 1}:\n{text}")
            lines.append(text)

    return " ".join(lines)
    



def print_doc(file_path):
    parra_lines = []
    # Open the .docx file
    doc = Document(file_path)
    # Extract and print text
    for paragraph in doc.paragraphs:
        parra_lines.append(paragraph.text)

    return " ".join(parra_lines)
# str_val = print_pdf(file_path)
# print(str_val)
  # PyMuPDF


def get_text_area_percentage(pdf_path):
    pdf_document = fitz.open(pdf_path)
    total_document_area = 0
    total_text_area = 0

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)

        # Page dimensions
        rect = page.rect
        total_page_area = rect.width * rect.height
        total_document_area += total_page_area  # Accumulate total document area

        # Extract text blocks
        text_blocks = page.get_text("blocks")
        for block in text_blocks:
            if len(block) >= 6:  # Ensure block structure is as expected
                x0, y0, x1, y1, text, *_ = block
                if text.strip():  # Check if text is not empty
                    text_rect = fitz.Rect(x0, y0, x1, y1)  # Bounding box of text
                    total_text_area += text_rect.width * text_rect.height  # Accumulate text area

    # Calculate percentage of document covered by text
    return (total_text_area / total_document_area) * 100 if total_document_area > 0 else 0



def check_images_in_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    has_images = False

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        if image_list:
            has_images = True
            break

    return has_images


def classification(file_path):
    #TODO
    pass

def inspect_text_blocks(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)  # Load the first page
    blocks = page.get_text("blocks")
    for block in blocks:
        print(block)  # Print each block to inspect its structure


# inspect_text_blocks(file_path)
text_percentage = get_text_area_percentage(file_path)
print(f"Text occupies: {text_percentage:.2f}% of the page")