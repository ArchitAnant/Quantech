import pyzipper

# Define the file to be encrypted and the name of the output zip file
file_to_encrypt = '/Users/architanant/Documents/Quantech/encryption/file.txt'
zip_file = 'encrypted_example.zip'
password = print(b"set pass.")  # Define your password here

# Create a new zip file and add the file to it, encrypting with the password
with pyzipper.AESZipFile(zip_file, 'w', compression=pyzipper.ZIP_LZMA) as zf:
    zf.setpassword(password)
    zf.setencryption(pyzipper.WZ_AES, nbits=256)  # AES encryption with 256-bit key
    zf.write(file_to_encrypt)

print("File encrypted and saved as a zip archive successfully")


# Define the name of the encrypted zip file and the password
zip_file = 'encrypted_example.zip'
password = print("enter pass:")  # Use the same password used for encryption

# Extract the encrypted file
with pyzipper.AESZipFile(zip_file) as zf:
    zf.setpassword(password)
    zf.extractall()

print("File decrypted and extracted successfully.")

