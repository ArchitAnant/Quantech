from PIL import Image, ImageDraw, ImageFont

class MarksheetFiller:
    def __init__(self, image_path, font_path="arial.ttf"):
        self.image_path = image_path
        self.font_path = font_path
        self.bounding_boxes = {
            "Name": ((15, 145), (954, 174)), 
            "Roll No": ((170, 282), (321, 313)),
            "Department": ((20, 235), (798, 266)),
            "Name Of The Parent:": ((230, 613), (605, 620)),
            "Mobile Number Of The Parent": ((335, 674), (659, 698)),
            "Signature Of The Parent With Date": ((368, 739), (582, 750))
        }

    @staticmethod
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

    @staticmethod
    def calculate_new_bounding_box(text, bounding_box, font=None):
        """
        Adjusts the bounding box so the text is centered horizontally within it.
        
        :param text: The text to place inside the bounding box.
        :param bounding_box: The original bounding box as ((x1, y1), (x2, y2)).
        :param font: The font used to measure the text. Defaults to None (uses default font).
        :return: The new bounding box with adjusted x1 and x2 values for centering.
        """
        # Calculate the width of the text
        text_width = MarksheetFiller.get_text_width(text, font)

        # Unpack the bounding box
        (x1, y1), (x2, y2) = bounding_box

        # Calculate the width of the bounding box
        box_width = x2 - x1

        # Calculate the padding to center the text
        padding = (box_width - text_width) // 2

        # Adjust the bounding box to center the text
        new_x1 = x1 + padding

        return (new_x1, y1), (x2, y2)

    def add_text_to_image(self, user_data):
        """
        Adds text to an image, placing the text inside given bounding boxes.
        
        :param user_data: Dictionary containing field names and corresponding text.
        """
        # Load the image
        img = Image.open(self.image_path)
        draw = ImageDraw.Draw(img)
        
        # Load the font
        font = ImageFont.truetype(self.font_path, size=20)

        # Iterate over each field and its corresponding bounding box
        for field, text in user_data.items():
            if field in self.bounding_boxes:
                bounding_box = self.bounding_boxes[field]

                # Center text for the "Name" and "Department" fields
                if field in ["Name", "Department"]:
                    # Calculate the new bounding box for centering the text
                    new_bounding_box = self.calculate_new_bounding_box(text, bounding_box, font)
                    upper_left, lower_right = new_bounding_box
                else:
                    # Use the original bounding box without changing it
                    upper_left, lower_right = bounding_box

                x1, y1 = upper_left
                # Draw the text at the calculated position
                draw.text((x1, y1), text, font=font, fill="black")

        # Add fixed text for the "Signature Of The Parent With Date" field
        signature_box = self.bounding_boxes["Signature Of The Parent With Date"]
        upper_left, lower_right = signature_box
        x1, y1 = upper_left
        draw.text((x1, y1), "[Digital Sign]", font=font, fill="black")

        # Save the resulting image
        img.save("filled_marksheet.png")
        img.show()

    @staticmethod
    def get_user_input():
        """
        Prompts the user for input to fill in the fields on the marksheet.
        
        :return: A dictionary containing the user input for each field.
        """
        user_data = {
            "Name": input("Enter Name: "),
            "Roll No": input("Enter Roll No: "),
            "Department": input("Enter Department: "),
            "Name Of The Parent:": input("Enter Name Of The Parent: "),
            "Mobile Number Of The Parent": input("Enter Mobile Number Of The Parent: "),
        }
        return user_data

# Usage example:
# if __name__ == "__main__":
#     image_path = "NOC.jpg"
#     filler = MarksheetFiller(image_path)
#     user_data = MarksheetFiller.get_user_input()
#     filler.add_text_to_image(user_data)