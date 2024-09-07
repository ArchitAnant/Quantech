from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import csv
import base64
from getpass import getpass

# Function to derive a key from a password using PBKDF2
def derive_key_from_password(password, salt, length=32):
    """
    Derive a cryptographic key from a password using PBKDF2.
    
    :param password: User's password as a string
    :param salt: A random salt (16 bytes recommended)
    :param length: The length of the derived key (default 32 bytes for AES-256)
    :return: A derived key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())  # Derive the key from the password (must be bytes)
    return key

# Function to encrypt a file
def encrypt_file(password, input_file, output_file):
    """
    Encrypt a file using AES (CBC mode) with a key derived from a password.
    
    :param password: The user's password
    :param input_file: The path to the plaintext input file
    :param output_file: The path where the encrypted file will be saved
    """
    # Generate a random salt (16 bytes) and IV (Initialization Vector)
    salt = os.urandom(16)
    iv = os.urandom(16)

    # Derive the key from the password and salt
    key = derive_key_from_password(password, salt)

    # Create a cipher object using the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Read the plaintext data from the input file
    with open(input_file, 'rb') as f:
        plaintext_data = f.read()

    # Pad the plaintext to be a multiple of 16 bytes (AES block size)
    padding_length = 16 - (len(plaintext_data) % 16)
    padded_data = plaintext_data + bytes([padding_length] * padding_length)

    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Write the salt, IV, and encrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(salt)  # Write the salt (16 bytes)
        f.write(iv)    # Write the IV (16 bytes)
        f.write(encrypted_data)  # Write the encrypted data

    print(f"File '{input_file}' successfully encrypted to '{output_file}'")

# Example usage
# if __name__ == "__main__":
#     # Get the password input from the user (secure input, no echo)
#     password = getpass("Enter password: ")

#     input_file = "plaintext_file.txt"  # Path to the plaintext file to encrypt
#     output_file = "encrypted_file.bin"  # Path to save the encrypted file

#     # Call the encryption function
#     encrypt_file(password, input_file, output_file)


# Take the password as user input securely

def read_csv():
    #read the csv which has which has id,name and isSecured
    with open('/Users/architanant/Documents/Quantech/encryption/datafile.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
            if row[2] == '1':
                choice = input("The file is secured\nWould you like to open the file? (y/n)")
                if choice == 'y':
                    password = getpass("Enter password: ")
                    decrypt_file_and_print(password,'/Users/architanant/Documents/Quantech/temp_out.txt',"yt.txt")

            else:
                if row[2] == '0':
                    choice = input("The file is not encrypted\nWhould you encrypt the file(y/n)?: ")
                    if choice == 'y':
                        password = getpass("Enter password: ")
                        encrypt_file(password,row[1],"temp_out.txt")
        


# Function to decrypt a file
def decrypt_file_and_print(password, input_file, output_file):
    """
    Decrypt a file using AES (CBC mode) with a key derived from a password, 
    save the decrypted content to a file, and print the content.
    
    :param password: The user's password
    :param input_file: The path to the encrypted input file
    :param output_file: The path where the decrypted file will be saved
    """
    # Read the salt and IV from the input file
    with open(input_file, 'rb') as f:
        salt = f.read(16)  # Read the salt (first 16 bytes)
        iv = f.read(16)    # Read the IV (next 16 bytes)
        encrypted_data = f.read()  # The remaining is the encrypted data

    # Derive the key from the password and salt
    key = derive_key_from_password(password, salt)

    # Create a cipher object using the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding
    padding_length = decrypted_padded_data[-1]
    decrypted_data = decrypted_padded_data[:-padding_length]

    # Write the decrypted data to the output file
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

    # Print the decrypted content
    print("Decrypted Content:")
    print(decrypted_data.decode('utf-8'))  # Assuming the decrypted data is in UTF-8 text format

    print(f"File '{input_file}' successfully decrypted to '{output_file}'")


# password = getpass("Enter password: ")
# decrypt_file_and_print(password,'/Users/architanant/Documents/Quantech/temp_out.txt',"yp.txt")