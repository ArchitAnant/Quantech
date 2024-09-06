import cv2
from PIL import Image, ImageDraw, ImageFont

def get_text_width(text, font=None):
    """
    Returns the total width of the given text string, including spaces.
    
    :param text: The text to measure.
    :param font: The font to use. If None, the default font is used.
    :return: The total width of the text in pixels.
    """
    if font is None:
        font = ImageFont.load_default()

    # Create a dummy image to measure the text
    image = Image.new("RGB", (200, 100), "white")
    draw = ImageDraw.Draw(image)

    # Calculate the total width of the text
    total_width = 0
    for char in text:
        bbox = draw.textbbox((0, 0), char, font=font)
        char_width = bbox[2] - bbox[0]
        total_width += char_width

    return total_width

def calculate_new_bounding_box(text, bounding_box, font=None):
    """
    Adjusts the bounding box so the text is centered horizontally within it.
    
    :param text: The text to place inside the bounding box.
    :param bounding_box: The original bounding box as ((x1, y1), (x2, y2)).
    :param font: The font used to measure the text. Defaults to None (uses default font).
    :return: The new bounding box with adjusted x1 and x2 values for centering.
    """
    # Calculate the width of the text
    text_width = get_text_width(text, font)

    # Unpack the bounding box
    (x1, y1), (x2, y2) = bounding_box

    # Calculate the width of the bounding box
    box_width = x2 - x1

    # Calculate the padding to center the text
    padding = (box_width - text_width) // 2

    # Adjust the bounding box to center the text
    new_x1 = x1 + padding

    return (new_x1, y1), (x2, y2)

def add_text_to_image(image_path, user_data, bounding_boxes, font_path="arial.ttf"):
    """
    Adds text to an image, placing the text inside given bounding boxes.
    
    :param image_path: path to the base image (marksheet)
    :param user_data: dictionary containing field names and corresponding text
    :param bounding_boxes: dictionary containing field names and their corresponding bounding box
    :param font_path: path to the font file used for the text
    """
    # Load the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Load the font
    font = ImageFont.truetype(font_path, size=20)

    # Iterate over each field and its corresponding bounding box
    for field, text in user_data.items():
        if field in bounding_boxes:
            bounding_box = bounding_boxes[field]

            # Center text for the "Name" and "Department" fields
            if field in ["Name", "Department"]:
                # Calculate the new bounding box for centering the text
                new_bounding_box = calculate_new_bounding_box(text, bounding_box, font)
                upper_left, lower_right = new_bounding_box
            else:
                # Use the original bounding box without changing it
                upper_left, lower_right = bounding_box

            x1, y1 = upper_left
            # Draw the text at the calculated position
            draw.text((x1, y1), text, font=font, fill="black")

    # Save the resulting image
    img.save("filled_marksheet.png")
    img.show()

# User data
user_data = {
    "Name": "ABCD",
    "Roll No": "2361000",
    "Department": "Cse AIML",
    "Name Of The Parent:": "ABCD",
    "Mobile Number Of The Parent": "973236XXXX",
    "Signature Of The Parent With Date": "[Digitaly Signed]"
}

# Bounding boxes
bounding_boxes = {
    "Name": ((15, 145), (954, 174)), 
    "Roll No": ((170, 282), (321, 313)),
    "Department": ((20, 235), (798, 266)),
    "Name Of The Parent:": ((230, 613), (605, 620)),
    "Mobile Number Of The Parent": ((335, 674), (659, 698)),
    "Signature Of The Parent With Date":((368, 739), (582, 750))
}

# Example usage:
image_path = "NOC.jpg"

# Call the function
add_text_to_image(image_path, user_data, bounding_boxes)