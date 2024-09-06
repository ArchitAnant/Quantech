import fitz
def images_in_pdf():
    # return images_between_text, image_dimensions of the images at the end and beggining of every page of the pdf
    pdf_document = fitz.open("/Users/macbook/Documents/Quantech/file_processing/test_files/single_page.pdf")
    images_between_text = False
    image_dimensions = {}

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        if image_list:
            images_between_text = True
            break
        else:
            image_dimensions[f'page_{page_number}_start_image'] = page.get_image_list()[0][2]
            image_dimensions[f'page_{page_number}_end_image'] = page.get_image_list()[-1][2]

    
    return images_between_text, image_dimensions


  # PyMuPDF
def images_in_pdf(): 

    pdf_path = "/Users/macbook/Documents/Quantech/file_processing/test_files/single_page.pdf"
    pdf_document = fitz.open(pdf_path)

    # Iterate through each page in the PDF
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)  # Load a page
        images = page.get_images(full=True)  # Get all images on the page

        # Get the page height (needed to determine position)
        page_height = page.rect.height

        # If there are no images on the page
        if not images:
            print(f"Page {page_number + 1}: No images found")
            continue

        # Loop through the images on the page
        for image_index, image in enumerate(images):
            xref = image[0]  # Extract XREF (the image identifier in the PDF)
            image_details = pdf_document.extract_image(xref)  # Extract the image details
            
            # Extract image dimensions
            width = image_details['width']
            height = image_details['height']

            # Get image position (bounding box)
            img_rects = page.get_image_rects(xref)
            
            for rect in img_rects:
                # Get the top-left corner (x0, y0) and bottom-right corner (x1, y1)
                x0, y0 = rect[0], rect[1]  # Top-left corner
                x1, y1 = rect[2], rect[3]  # Bottom-right corner
                
                # Determine the vertical position of the image
                image_middle_y = (y0 + y1) / 2  # The middle y-coordinate of the image

                # Divide the page into top, middle, and bottom thirds
                if image_middle_y >= (2/3) * page_height:
                    position = "Top"
                elif image_middle_y >= (1/3) * page_height:
                    position = "Middle"
                else:
                    position = "Bottom"

                print(f"Page {page_number + 1}, Image {image_index + 1}:")
                print(f"  Dimensions: {width}x{height} pixels")
                print(f"  Position: {position} (y-coordinate: {image_middle_y})")

    pdf_document.close()


            
print(images_in_pdf())
