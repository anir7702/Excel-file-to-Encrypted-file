import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

IV_LENGTH = 16
def aes256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

def aes256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data

def decode_base64_to_excel(encoded_content):
    try:
        return base64.b64decode(encoded_content)
    except Exception as e:
        raise RuntimeError(f"Error encoding file: {e}")

def encrypt_file(input_file, server):
    try:
        if server == 'prod':
            key = b"<your key>"
        else:
            key = b"<your key>"
        iv = key[:16]
        with open(input_file, 'rb') as excel_file:
            data = excel_file.read()
        encrypted_data = aes256_encrypt(data, key, iv)
        if encrypted_data:  
            ip_name = os.path.basename(input_file)
            file_path = f"encrypted_files/{os.path.splitext(ip_name)[0]}.xlsx"            
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)
            print(f"File {file_path} encrypted successfully.")
        else:
            print("Encryption failed. No data generated.")
    except Exception as e:
        raise RuntimeError(f"Error during encryption: {e}")

def encrypt_files_from_folder(folder_path, server):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            input_file = os.path.join(folder_path, file_name)
            encrypt_file(input_file, server)
folder_path = r'<your folder path>'
server = 'prod'  
encrypt_files_from_folder(folder_path, server)
