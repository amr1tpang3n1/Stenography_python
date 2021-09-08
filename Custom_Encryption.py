def Encrypt_Ceaser_cipher(data,key):
    encrypted_string = ""
    for i in data:
        encrypt = ord(i) + key
        encrypt = chr(encrypt)
        encrypted_string += encrypt

    return encrypted_string

def Decrypt_rot_13(data,key):
    decrypted_string = ""
    for i in data:
        encrypt = ord(i) - key
        encrypt = chr(encrypt)
        decrypted_string += encrypt

    return decrypted_string