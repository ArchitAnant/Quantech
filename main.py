import os

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

