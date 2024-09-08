from img2table.ocr import TesseractOCR, EasyOCR
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfgen import canvas
import cv2
import numpy as np
from img2table.document import Image as Img2TableImage
from img2table.ocr import TesseractOCR
from pdf2image import convert_from_path
import pandas as pd
import os
from tempfile import NamedTemporaryFile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class ImageTableExtractor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.img = Img2TableImage(src=image_path)
        self.tesseract = TesseractOCR()
        self.tables = self.img.extract_tables(ocr=self.tesseract, borderless_tables=True)

    def extract_tables(self):
        return self.tables

    def draw_table(self, canvas, df, page_width, page_height):
        # Convert dataframe to list of lists for ReportLab Table, including the header
        table_data_list = [df.columns.tolist()] + df.values.tolist()

        # Create Table with fixed font size
        font_size = 10
        table = Table(table_data_list)

        # Set Table Style
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), font_size),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Calculate table width and height
        available_width = page_width - 2 * 72  # 1-inch margins on both sides
        available_height = page_height - 2 * 72  # 1-inch margins on top and bottom
        table_width, table_height = table.wrapOn(canvas, available_width, available_height)

        # Draw Table on Canvas, centered on the page
        x = (page_width - table_width) / 2
        y = (page_height - table_height) / 2
        table.drawOn(canvas, x, y)

    def create_pdf_with_tables(self, output_path):
        # Create a new PDF
        c = canvas.Canvas(output_path)
        page_width, page_height = c._pagesize

        for i, table in enumerate(self.tables):
            df = table.df
            self.draw_table(c, df, page_width, page_height)
            
            # Start a new page for the next table, except for the last one
            if i < len(self.tables) - 1:
                c.showPage()

        c.save()

# #Sample Usage
# extractor = ImageTableExtractor("1234.png")
# tables = extractor.extract_tables()
# extractor.create_pdf_with_tables("output_tables.pdf")

# print("Extracted tables:")
# for i, table in enumerate(tables):
#     print(f"Table {i + 1}:")
#     print(table.df)
#     print("\n")

class PdfTableExtractor:
    def __init__(self, file_path, dpi=200, start_page=1, end_page=None):
        self.file_path = file_path
        self.dpi = dpi
        self.start_page = start_page
        self.end_page = end_page
        self.opencv_images = []
        self.table_data = {}
        self.page_tables = {}
        self.detect_format()

    def detect_format(self):
        """Detect the file format and load images accordingly."""
        try:
            if self.file_path.lower().endswith('.pdf'):
                self.load_pdf_images()
            elif self.file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.load_image_file()
            else:
                raise ValueError("Unsupported file type. Only PDF and image files (PNG, JPG, JPEG) are supported.")
        except Exception as e:
            print(f"Error detecting format: {e}")
            raise

    def load_pdf_images(self):
        """Load images from PDF file."""
        try:
            images = convert_from_path(self.file_path, dpi=self.dpi)
            
            total_pages = len(images)
            print(f"Total pages in PDF: {total_pages}")
            
            if self.start_page < 1:
                raise ValueError(f"Invalid start_page: {self.start_page}. Must be >= 1.")
            
            if self.end_page is None:
                self.end_page = total_pages
            elif self.end_page > total_pages:
                print(f"Warning: end_page ({self.end_page}) is greater than total pages ({total_pages}). Setting end_page to {total_pages}.")
                self.end_page = total_pages
            
            if self.start_page > self.end_page:
                raise ValueError(f"Invalid page range: start_page ({self.start_page}) > end_page ({self.end_page})")
            
            print(f"Processing pages {self.start_page} to {self.end_page}")
            
            self.opencv_images = [cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY) for image in images[self.start_page-1:self.end_page]]
            print(f"Loaded {len(self.opencv_images)} pages")
        except Exception as e:
            print(f"Error loading PDF images: {e}")
            raise

    def load_image_file(self):
        """Load image file directly."""
        try:
            if not os.path.isfile(self.file_path):
                raise FileNotFoundError(f"The file at {self.file_path} does not exist.")
            image = cv2.imread(self.file_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                raise ValueError(f"Error loading the image at {self.file_path}.")
            self.opencv_images = [image]
        except Exception as e:
            print(f"Error loading image file: {e}")
            raise

    def extract_tables(self, image):
        """Extract table regions from the image."""
        with NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_path = temp_file.name
            cv2.imwrite(temp_path, image)
        try:
            img = Img2TableImage(src=temp_path)
            extracted_tables = img.extract_tables(ocr=TesseractOCR(), implicit_rows=True, implicit_columns=True)
        except Exception as e:
            print(f"Error extracting tables: {e}")
            extracted_tables = []
        finally:
            os.remove(temp_path)
        
        return extracted_tables

    def get_data_frames_for_page(self, page_number):
        """Retrieve the list of DataFrames for a specific page."""
        if page_number not in self.page_tables:
            if page_number <= len(self.opencv_images):
                image = self.opencv_images[page_number - self.start_page]
                if image is None or image.size == 0:
                    print(f"Warning: Empty or invalid image for page {page_number}")
                    return []
                try:
                    extracted_tables = self.extract_tables(image)
                    self.page_tables[page_number] = []
                    for j, table in enumerate(extracted_tables):
                        df = table.df
                        self.table_data[(page_number, j + 1)] = {
                            'coordinates': (table.bbox.x1, table.bbox.y1, table.bbox.x2, table.bbox.y2),
                            'data_frame': df
                        }
                        self.page_tables[page_number].append(df)
                except Exception as e:
                    print(f"Error processing page {page_number}: {e}")
            else:
                print(f"Warning: Page number {page_number} is out of range. Total pages: {len(self.opencv_images)}")

        return self.page_tables.get(page_number, [])

    def process_all_pages(self):
        """Process all pages and return a dictionary of results."""
        results = {}
        for page_number in range(self.start_page, self.end_page + 1):
            try:
                data_frames = self.get_data_frames_for_page(page_number)
                results[page_number] = data_frames
                print(f"Processed page {page_number}: Found {len(data_frames)} tables")
            except Exception as e:
                print(f"Error processing page {page_number}: {e}")
                results[page_number] = []
        return results

    def create_pdf_from_tables(self, output_filename="extracted_tables.pdf"):
        """
        Create a PDF file containing all extracted tables, with each table on a separate page.
        """
        doc = SimpleDocTemplate(output_filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        for page, tables in self.page_tables.items():
            for table_num, df in enumerate(tables, 1):
                # Add a title for each table
                title = f"Page {page}, Table {table_num}"
                elements.append(Paragraph(title, styles['Heading1']))
                elements.append(Spacer(1, 12))  # Add some space after the title

                # Convert DataFrame to a list of lists
                data = [df.columns.tolist()] + df.values.tolist()
                
                # Create a Table object
                table = Table(data)
                
                # Add style to the table
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ])
                table.setStyle(style)
                
                elements.append(table)
                elements.append(Spacer(1, 30))  # Add space after the table

        # Build the PDF
        doc.build(elements)
        print(f"PDF created successfully: {output_filename}")

# Usage example
# processor = PdfTableExtractor("basic-text.pdf", start_page=1, end_page=1)  
# all_results = processor.process_all_pages()

# for page, tables in all_results.items():
#     print(f"Page {page}: {len(tables)} tables found")
#     for i, df in enumerate(tables, 1):
#         print(f"  Table {i} shape: {df.shape}")

# processor.create_pdf_from_tables("output_tables.pdf")