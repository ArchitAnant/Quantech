import os
from file_processing.machine_readablity import is_machine_readable
from file_processing.readablity import read_doc,read_pdf
from searching import search
from translation.translation import translate_text
from tts.basic_tts import save_mp3
from encryption.password_encryp import read_csv
from searching.searching import find_word_location
from standardisation.table_extract import PdfTableExtractor,ImageTableExtractor
from standardisation.pdftocsv import read_csv
from standardisation import tomachinereadable




# Define file path
file_path = input("Please enter the file path: ")


def automation(file_path):
     '''
    l[0]  1 : standardisation
          2 : search
    l[1]  1 : Decrypt
          2 : Search
          3 : Text to Speech
    l[2]  1 : Text to Speech
          2 : Translation 
     '''
     l=[]
     print("1.Standardisation\n2.Search")
     user_choice=int(input("Enter choice no."))
     if user_choice==1:
          l.append(1)
          print("Choices:\n1.Decrypt\n2.Search\n3.Exit")
          user_choice1=int(input("Enter choice:"))
          if user_choice1==1:
               l.append(1)
               print("Choices:\n1.Text to Speech\n2.Translation\n3.Exit")
               user_choice2=int(input("Enter choice:"))
               if user_choice2==1:
                    l.append(1)
               elif user_choice==2:
                    l.append(2)
               else:
                    return l
          elif user_choice1==2:
               l.append(2)
               print("Choices:\n1.Text to Speech\n2.Translation\n3.Exit")
               user_choice2=int(input("Enter choice:"))
               if user_choice2==1:
                    l.append(1)
               elif user_choice==2:
                    l.append(2)
               else:
                    return l
          else:
               return l
     else:
        l.append(2)
        print("Choices:\n1.Text to Speech\n2.Exit")
        user_choice=int(input("Enter choice:"))
        if user_choice==1:
             l.append(1)
        else:
             return l
     return l
          
               
def perform_auto(file_path,l):
     if l[0]==1:
          if l[1]==1:
               if l[2]==1:
                    read_csv(file_path)
               else:
                    translated_output = translate_text(input_text, tgt_lang)
                    print(translated_output)
          else:
               word = input("Enter the word to search: ")
               results = find_word_location(file_path, word)
               print(results)
     else:
          if l[1]==1:
               save_mp3(input_text)
          else:
               if l[2]==1:
                    input_text = read_pdf(file_path)
               else:
                    translated_output = translate_text(input_text, tgt_lang)
                    print(translated_output)

# Check if file exists
if os.path.exists(file_path):
    print(f'The file "{file_path}" exists.')
else:
    print(f'The file "{file_path}" does not exist.')


if(is_machine_readable(file_path)==True):
     print ("File is  machine readable.")
else:
     print("file is non machine readable.")
     

print("Operations:\n1.Searching\n 2.Standardisation\n 3.Translation\n 4.Text to Speech\n 5.Encryption & Decription\n 6.Automation\n 7. exit")
choice=int(input("Enter choice no:"))
if choice==1:
    print("Options\n 1.Absolute searching\n2.Dynamic Searching")
    opt1=int(input("Enter option no:"))
    if opt1==1:
        word = input("Enter the word to search: ")
        results = find_word_location(file_path, word)
        print(results)
        #absolute
    else:
        query = input("Enter your query: ")
        search.process_pdf_and_query(file_path,query)
                #dynamic
    
elif choice==2:
     print("Options\n 1.Tabular\n2.Non Tabular\n3. Formatting")
     opt2=int(input("Enter option no:"))
     if opt2==1:
        #tabular
        #create table from pdf
        print("Options\n 1.from pdf\n2.from img\n3. Formatting")
        ch = int(input("Enter choice no:"))
        if ch == 1:
          processor1 = PdfTableExtractor("basic-text.pdf", start_page=1, end_page=1)   
          all_results = processor1.process_all_pages()

          for page, tables in all_results.items():
               print(f"Page {page}: {len(tables)} tables found")
               for i, df in enumerate(tables, 1):
                    print(f"  Table {i} shape: {df.shape}")

               processor1.create_pdf_from_tables("output_tables.pdf")
        elif ch==2:
             processor2 = ImageTableExtractor("1234.png", start_page=1, end_page=1)
             tables = processor2.extract_tables()
             processor2.create_pdf_with_tables("output_tables.pdf")
             print("Extracted tables:")
             for i, table in enumerate(tables):
               print(f"Table {i + 1}:")
               print(table.df)
               print("\n")
        else:
             read_csv(file_path)

     else:
        tomachinereadable.convert_to_machine_readable(file_path, "output.pdf")




elif choice==3:
     if ".doc" in file_path:
          input_text = read_doc(file_path)
     else:
          input_text = read_pdf(file_path)
     tgt_lang = input("Enter the target language code (e.g., 'ben_Beng' for Bengali): ")
     translated_output = translate_text(input_text, tgt_lang)
     print(translated_output)


elif choice==4:
     if ".doc" in file_path:
          input_text = read_doc(file_path)
     else:
          input_text = read_pdf(file_path)
     save_mp3(input_text)
      #tts
elif choice==5:
     read_csv()

elif choice==6:
     print("Exiting") 
elif choice==7:
     print("Exiting") 
else:
     print("Invalid Choice")     

