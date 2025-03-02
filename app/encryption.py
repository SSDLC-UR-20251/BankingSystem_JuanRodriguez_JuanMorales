from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256


def hash_with_salt(texto):
    # Generar un salt aleatorio
    salt = get_random_bytes(16)

    # Convertir el texto en claro a bytes
    texto_bytes = texto.encode('utf-8')

    # Crear un objeto de hash SHA-256
    hash_obj = SHA256.new()

    # Agregar la sal y el texto plano al hash
    hash_obj.update(salt)
    hash_obj.update(texto_bytes)

    # Calcular el hash final
    hash_result = hash_obj.digest()

    # Devolver el hash
    return hash_result.hex(), salt.hex()


def decrypt_aes(texto_cifrado_str, nonce_str, clave):
    if isinstance(texto_cifrado_str, list):  # Si es una lista, conviértelo en una cadena
        texto_cifrado_str = texto_cifrado_str[0]  # O usa ''.join(texto_cifrado_str) si hay múltiples elementos

    if isinstance(nonce_str, list):
        nonce_str = nonce_str[0]  

    # Convertir los valores de string a bytes
    texto_cifrado = bytes.fromhex(texto_cifrado_str)
    nonce = bytes.fromhex(nonce_str)

    cipher = AES.new(clave, AES.MODE_EAX, nonce=nonce)
    texto_descifrado = cipher.decrypt(texto_cifrado)

    return texto_descifrado.decode()



def compare_salt(text, hash, salt):
    salt = bytes.fromhex(salt)
    # Convertir el texto en claro a bytes
    texto_bytes = text.encode('utf-8')
    # Crear un objeto de hash SHA-256
    hash_obj = SHA256.new()
    # Agregar la sal y el texto plano al hash
    hash_obj.update(salt)
    hash_obj.update(texto_bytes)
    # Calcular el hash final
    hash_result = hash_obj.digest()
    # convertimos a hex
    final = hash_result.hex()
    print("final" + final)
    if final == hash:
        return True
    else:
        return False


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

# Función para ofuscar el DNI
def ofuscar_dni(dni):
    return '*' * (len(dni) - 4) + dni[-4:]

# Funcion para desencriptar y mostrar solo los ultimos 4 digitos
def cuatro_digitos(texto_cifrado_str, nonce_str, clave):
    texto = decrypt_aes(texto_cifrado_str, nonce_str, clave)  
    
    if len(texto) < 9:  
        return "******" 

    res = "******" + texto[6:10] 
    return res



def hash_salt(texto, salt):
   
    if isinstance(salt, str):
        salt = bytes.fromhex(salt)  

    
    try:
        texto_bytes = bytes.fromhex(texto)  
    except ValueError:
        texto_bytes = texto.encode()  

    hash_obj = SHA256.new(texto_bytes + salt)
    return hash_obj.hexdigest()


if __name__ == '__main__':
    texto = "Hola Mundo"
    clave = get_random_bytes(16)
    texto_cifrado, nonce = encrypt_aes(texto, clave)
    print("Texto cifrado: " + texto_cifrado)
    print("Nonce: " + nonce)
    des = decrypt_aes(texto_cifrado, nonce, clave)
    print("Texto descifrado: " + des)
    password = "password"
    pwd_hash = hash_with_salt(password)
    print("Hash: " + pwd_hash[0])
    password_other = "password"
    print("Hash: " + hash_with_salt(password_other)[0])