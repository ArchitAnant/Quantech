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

# Example usage
if _name_ == "_main_":
    input_text = "This is an example text that needs to be translated. " * 50  # Large input text
    tgt_lang = input("Enter the target language code (e.g., 'ben_Beng' for Bengali): ")
    translated_output = translate_text(input_text, tgt_lang)
    print(translated_output)