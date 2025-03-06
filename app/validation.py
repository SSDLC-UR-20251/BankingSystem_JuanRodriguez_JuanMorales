from _datetime import datetime
import re
import unicodedata


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
