import fitz

def find_word_location(pdf_path, search_word):
    matches = []
    search_word = search_word.lower()

    try:
        with fitz.open(pdf_path) as doc:
            for page_num, page in enumerate(doc):
                words = page.get_text("words")  # Get all words on the page
                words.sort(key=lambda w: (w[1], w[0]))  # Sort words by y-coordinate, then x-coordinate
                
                # Calculate custom line numbers
                line_height = 12  # Approximate line height, adjust if needed
                current_line = 1
                last_y = words[0][1] if words else 0
                
                for word in words:
                    x0, y0, x1, y1, text, block_no, _, word_no = word
                    
                    # Update line number if y-coordinate difference is significant
                    if y0 - last_y > line_height / 2:
                        current_line += 1
                    last_y = y0
                    
                    if search_word in text.lower():
                        # Get surrounding text for context
                        surrounding_text = page.get_text("text", clip=(x0-50, y0-10, x1+50, y1+10))
                        
                        matches.append({
                            "page": page_num + 1,
                            "line": current_line,
                            "text": text,
                            "context": surrounding_text.strip()
                        })
    except Exception as e:
        print(f"Error processing PDF: {e}")
    
    return matches

# Example Usage:
# pdf_file = "basic-text.pdf"  # Replace with your actual PDF file path
# word_to_search = "Third"

# # Find word location
# results = find_word_location(pdf_file, word_to_search)

# # Output the results
# if results:
#     for result in results:
#         print(f"Found '{result['text']}' on Page {result['page']}, Line {result['line']}")
#         print(f"Context: {result['context']}")
#         print("---")
# else:
#     print(f"No occurrences of '{word_to_search}' found in the PDF.")