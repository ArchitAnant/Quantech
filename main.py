import os

# Define file path
file_path = input("Please enter the file path: ")

# Check if file exists
if os.path.exists(file_path):
    print(f'The file "{file_path}" exists.')
else:
    print(f'The file "{file_path}" does not exist.')
if   (is_machine_readable(file_path)==True):
     print ("File is  machine readable.")
else:
     print("file is non machine readable.")
     

print("Operations:\n1.Searching\n 2.Standardisation\n 3.Translation\n 4.Text to Speech\n 5.Encryption\n 6.Decryption")
choice=int(input("Enter choice no:"))
if choice==1:
    print("Options\n 1.Absolute searching\n2.Dynamic Searching")
    opt1=int(input("Enter option no:"))
    if opt1==1:
        #absolute
        pass
    else:
        #dynamic
        pass
elif choice==2:
     print("Options\n 1.Tabular\n2.Non Tabular")
     opt2=int(input("Enter option no:"))
     if opt2==1:
        #tabular
        pass
     else:
        #non tabular
        pass
elif choice==3:
      #translation
      pass
elif choice==4:
      #tts
      pass
elif choice==5:

     #encryption
     pass
elif choice==6:
     #decryption
     pass  
else:
     print("Invalid Choice")     

