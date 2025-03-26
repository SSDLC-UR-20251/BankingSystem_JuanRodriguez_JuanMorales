from _datetime import datetime
import re
import unicodedata
import unittest


def normalize_input(data):    
    return unicodedata.normalize("NFKD",data.strip())

# valido el email
def validate_email(email):
    email = normalize_input(email)
    pattern = r'^[a-zA-Z0-9._%+-]+@urosario\.edu\.co$'
    return re.match(pattern, email) is not None


# valido la edad
def validate_dob(dob):
    try:
        actual = datetime.now()
        fecha = datetime.strptime(dob, "%Y-%m-%d")
        
        if fecha > actual:
            return False  # Fecha en el futuro no válida
        
        edad = (actual - fecha).days // 365 
        return edad >= 16
    except ValueError:
        return False  # Maneja errores en el formato de fecha

# valido el usuario
def validate_user(user):
    user = normalize_input(user)
    pattern = r"^[a-zA-Z0-9.]{3,20}$"  # Solo letras, números y punto, longitud entre 3 y 20
    return re.match(pattern, user) is not None

# valido el dni
def validate_dni(dni):
    if not dni.isdigit():  # Verifica que sea numérico
        return False
    dni_valid = int(dni)
    return 1000000000 <= dni_valid <= 1999999999

# valido la contraseña
def validate_pswd(pswd):
    if not (8 <= len(pswd) <= 35):  # Acepta 8 y 35 caracteres
        return False

    has_upper = any(c.isupper() for c in pswd)
    has_lower = any(c.islower() for c in pswd)
    has_digit = any(c.isdigit() for c in pswd)
    has_special = any(c in "!@#$%^&*()-+=?" for c in pswd)  # Caracteres especiales comunes

    return has_upper and has_lower and has_digit and has_special


def validate_name(name):
    name = normalize_input(name)
    return bool(re.match(r"^[a-zA-Z\s]+$", name))

class TestValidationFunctions(unittest.TestCase):
    
    def test_validate_email(self):
        self.assertTrue(validate_email("usuario@urosario.edu.co"))
        self.assertFalse(validate_email("usuario@gmail.com"))
        self.assertFalse(validate_email("usuario@urosario.com"))
        self.assertFalse(validate_email("usuario@urosario.edu"))
        self.assertFalse(validate_email("@urosario.edu.co"))
    
    def test_validate_dob(self):
        self.assertTrue(validate_dob("2000-01-01"))  # Mayor de 16
        self.assertFalse(validate_dob("2010-01-01")) # Menor de 16
    
    def test_validate_user(self):
        self.assertTrue(validate_user("sara.palacios"))
        self.assertFalse(validate_user("sara_palacios"))
        self.assertFalse(validate_user("sarapalacios"))
        self.assertFalse(validate_user("sara.palacios1"))
        self.assertFalse(validate_user("sara.palacios!"))  # No debe contener caracteres especiales
    
    def test_validate_dni(self):
        self.assertTrue(validate_dni("1000000001"))
        self.assertFalse(validate_dni("9999999999"))
        self.assertFalse(validate_dni("10000000001"))
        self.assertFalse(validate_dni("abcdefg123"))
    
    def test_validate_name(self):
        self.assertTrue(validate_name("Sara"))
        self.assertTrue(validate_name("Palacios"))
        self.assertFalse(validate_name("Sara123"))
        self.assertFalse(validate_name("Sara_Palacios"))
        self.assertFalse(validate_name("Sara!"))
        self.assertFalse(validate_name("Sara Palacios"))  # No debe contener espacios
    
    def test_validate_password(self):
        self.assertTrue(validate_pswd("Passw0rd!"))  # Cumple con los requisitos
        self.assertFalse(validate_pswd("password"))  # Falta mayúscula, número y especial
        self.assertFalse(validate_pswd("PASSWORD1"))  # Falta minúscula y especial
        self.assertFalse(validate_pswd("Passw0rd"))  # Falta carácter especial
        self.assertFalse(validate_pswd("Pw1!"))  # Demasiado corta
        self.assertFalse(validate_pswd("A" * 36 + "1!"))  # Demasiado larga



if __name__ == "__main__":
    unittest.main()



