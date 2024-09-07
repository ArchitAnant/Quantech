from img2table.document import Image
from img2table.ocr import TesseractOCR, EasyOCR
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas

class TableExtractor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.img = Image(src=image_path)
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
# extractor = TableExtractor("1234.png")
# tables = extractor.extract_tables()
# extractor.create_pdf_with_tables("output_tables.pdf")

# print("Extracted tables:")
# for i, table in enumerate(tables):
#     print(f"Table {i + 1}:")
#     print(table.df)
#     print("\n")