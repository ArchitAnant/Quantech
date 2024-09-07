
import fitz  # PyMuPDF
from readablity import check_images_in_pdf, read_pdf
def return_layout(file_path):
    
    pdf_document = fitz.open(file_path)
    middle_list=[]
    height_list=[]
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
            is_middle=0
            for rect in img_rects:
                # Get the top-left corner (x0, y0) and bottom-right corner (x1, y1)
                x0, y0 = rect[0], rect[1]  # Top-left corner
                x1, y1 = rect[2], rect[3]  # Bottom-right corner
                
                # Determine the vertical position of the image relative to the top
                image_middle_y = (y0 + y1) / 2  # The middle y-coordinate of the image

                # Divide the page into top, middle, and bottom thirds relative to the top
                if image_middle_y <= (1/3) * page_height:
                    print("Top")
                    is_middle=0
                elif image_middle_y <= (2/3) * page_height:
                    print("Middle")
                    is_middle=1
                else:
                   print("Bottom")
                   is_middle=0
            middle_list.append(is_middle)
            height_list.append(height)
            
                
                
    pdf_document.close()
    return middle_list, height_list
            

def is_machine_readable(file_path):
    if not check_images_in_pdf(file_path):
        if len(read_pdf(file_path))==0:
            return False
        else:
            return True
    else:
        if len(read_pdf(file_path))==0:
            return False
        else:
            pos_list,dim_list=return_layout(file_path)
            for pos in pos_list:
                if pos ==0:
                    return False
            for height in dim_list:
                if height<=500:
                    return True
                #     if dim_list[i]<=500:
                #         return True
    return False
print(is_machine_readable("/Users/macbook/Documents/Quantech/file_processing/test_files/multifile-n.pdf"))
