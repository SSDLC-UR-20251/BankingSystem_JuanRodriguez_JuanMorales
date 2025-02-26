from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def hash_with_salt(texto):
   
    salt = get_random_bytes(16)
    
    texto_bytes = texto.encode()
    texto_bytes += salt
    hash = SHA256.new(texto_bytes)
    
    hash_result = hash.hexdigest()
    return hash_result

def decrypt_aes(texto_cifrado, nonce, clave):
    texto_cifrado_bytes = bytes.fromhex(texto_cifrado)
    nonce_bytes = bytes.fromhex(nonce)
    
    cipher = AES.new(clave, AES.MODE_EAX, nonce=nonce_bytes)
    
    texto_descifrado_bytes = cipher.decrypt(texto_cifrado_bytes)
    texto_descifrado = texto_descifrado_bytes.decode()


def encrypt_aes(texto, clave):
    # Convertir el texto a bytes
    texto_bytes = texto.encode()

    # Crear un objeto AES con la clave proporcionada
    cipher = AES.new(clave, AES.MODE_EAX)

    # Cifrar el texto
    nonce = cipher.nonce
    texto_cifrado, tag = cipher.encrypt_and_digest(texto_bytes)

    # Convertir el texto cifrado en bytes a una cadena de texto
    texto_cifrado_str = texto_cifrado.hex()

    # Devolver el texto cifrado y el nonce
    return texto_cifrado_str, nonce.hex()

if __name__ == '__main__':
    texto = "Hola Mundo"
    clave = get_random_bytes(16)
    texto_cifrado, nonce = encrypt_aes(texto, clave)
    print("Texto cifrado: " + texto_cifrado)
    print("Nonce: " + nonce)
    des = decrypt_aes(texto_cifrado, nonce, clave)
    print("Texto descifrado: " + des)