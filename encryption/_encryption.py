import pyzipper
import getpass

# Take the password as user input securely
password = getpass.getpass(prompt='Set password: ').encode('utf-8')
file_names = []

# Define the file to be encrypted and the name of the output zip file
file_to_encrypt = '/Users/architanant/Documents/Quantech/encryption/file.txt'
zip_file = 'encrypted_example.zip'

def encrypt(zipname, filename, password):

    with pyzipper.AESZipFile(zipname, 'w', compression=pyzipper.ZIP_LZMA) as zf:
        zf.setpassword(password)
        zf.setencryption(pyzipper.WZ_AES, nbits=256)  # AES encryption with a 256-bit key
        zf.write(filename)
        file_names = zf.namelist()
    
    print("File encrypted and saved as a zip archive successfully.")



# save the file names in the csv. so as to acess them later rathen than printing it
print(file_names)

# Take the password as user input securely
password = getpass.getpass(prompt='Enter password: ').encode('utf-8')

# Define the name of the encrypted zip file and the name of the output file
zip_file = '/Users/architanant/Documents/Quantech/encryption/file.txt'
output_file = '/Users/architanant/Documents/Quantech/encryption/file.txt'

# Extract the encrypted file
def decrypt(zip_file, output_file, password):
    try:
        with pyzipper.AESZipFile(zip_file) as zf:
            zf.setpassword(password)
            zf.extract(output_file) 
            # print(zf.read('/Users/macbook/Documents/Quantech/encryption/file.txt')) # Extracts all files in the zip archive
            print(f"File decrypted and extracted successfully.")

        # Display the content of the decrypted file
        with open(output_file, 'r') as file:
            content = file.read()
            print("\nDecrypted file content:")
            print(content)

    except RuntimeError:
        print("Incorrect password or file is corrupted.")
    except FileNotFoundError:
        print("Decrypted file not found.")




e = encrypt(zip_file, file_to_encrypt, password)
d = decrypt(zip_file, output_file, password)
