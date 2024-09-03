import pyzipper
import getpass

# Take the password as user input securely
password = getpass.getpass(prompt='Set password: ').encode('utf-8')

# Define the file to be encrypted and the name of the output zip file
file_to_encrypt = '/Users/macbook/Documents/Quantech/encryption/file.txt'
zip_file = 'encrypted_example.zip'

# Create a new zip file and add the file to it, encrypting with the password
with pyzipper.AESZipFile(zip_file, 'w', compression=pyzipper.ZIP_LZMA) as zf:
    zf.setpassword(password)
    zf.setencryption(pyzipper.WZ_AES, nbits=256)  # AES encryption with 256-bit key
    zf.write(file_to_encrypt)

print("File encrypted and saved as a zip archive successfully.")


# Take the password as user input securely
password = getpass.getpass(prompt='Enter password: ').encode('utf-8')

# Define the name of the encrypted zip file and the name of the output file
zip_file = 'encrypted_example.zip'
output_file = 'decrypted_example.txt'

# Extract the encrypted file
with pyzipper.AESZipFile(zip_file) as zf:
    zf.setpassword(password)
    try:
        zf.extractall()  # This will extract all files in the zip
        print(f"File decrypted and extracted successfully.")
    except RuntimeError:
        print("Incorrect password or file is corrupted.")


# Define the name of the encrypted zip file and the password


