from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load the model and tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

# Initialize the translation pipeline
translator = pipeline('translation', model=model, tokenizer=tokenizer, max_length=400, device=-1)

def translate_text(input_text, tgt_lang):
    try:
        # Split the input text into chunks of 400 characters
        chunks = [input_text[i:i + 400] for i in range(0, len(input_text), 400)]
        translated_chunks = []
        
        # Translate each chunk and store the result
        for chunk in chunks:
            translated_text = translator(chunk, src_lang='eng_Latn', tgt_lang=tgt_lang)[0]['translation_text']
            translated_chunks.append(translated_text)
        
        # Concatenate all translated chunks into one string
        final_translation = ' '.join(translated_chunks)
        return final_translation

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# # Example usage
# if _name_ == "_main_":
#     input_text = "This is an example text that needs to be translated. " * 50  # Large input text
#     tgt_lang = input("Enter the target language code (e.g., 'ben_Beng' for Bengali): ")
#     translated_output = translate_text(input_text, tgt_lang)
#     print(translated_output)
# Initialize the translation pipeline
translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang='eng_Latn', tgt_lang='ben_Beng', max_length=400,device=0)

def translate_docx(input_docx, src_lang, tgt_lang, output_docx, encoding='utf-8'):
    try:
        # Load the input .docx file
        document = Document(input_docx)
        translated_doc = Document()

        # Iterate over each paragraph in the document
        for paragraph in document.paragraphs:
            text_content = paragraph.text

            # Translate the text content
            if text_content.strip():  # Check if the paragraph is not empty
                translated_text = translator(text_content)[0]['translation_text']
                translated_doc.add_paragraph(translated_text)
            else:
                translated_doc.add_paragraph("")  # Add a blank paragraph for empty lines

        # Save the translated content to the output .docx file
        translated_doc.save(output_docx)

        print(f"Translated content saved to '{output_docx}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_docx}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# # User input for source and target languages
# src_lang = 'eng_Latn'
# tgt_lang = 'asm_Beng'

# # Input DOCX file path
# input_docx = '/content/Rabindranath Tagore.docx'

# # Output DOCX file path
# output_docx = 'translated_output2.docx'

# # Call the translation function
# translate_docx(input_docx, src_lang, tgt_lang, output_docx)