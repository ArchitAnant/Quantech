import PyPDF2
import pypandoc
import os
# Open the PDF file
with open("example.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    
    # Iterate through the pages
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()
        print(f"Page {page_num + 1}:\n{text}")




def read_doc_file(file_path):
    output = pypandoc.convert_file(file_path, 'plain')
    return output

file_path = "example.doc"
text = read_doc_file(file_path)
print(text)

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except OSError as e:
        print(f"Error: {e}")
        return None

file_path = "example.txt"  # Replace with your file path
size_in_bytes = get_file_size(file_path)
if size_in_bytes is not None:
    print(f"The size of the file is {size_in_bytes} bytes.")
else:
    print("Could not retrieve file size.")