from _datetime import datetime
import re
import unicodedata


def normalize_input(data):    
    return unicodedata.normalize("NFKD",data.strip())


# valido el email
def validate_email(email):
    
    email = normalize_input(email)
    return True


# valido la edad
def validate_dob(dob):
    actual = datetime.now()
    fecha = datetime.strptime(dob, "%Y-%m-%d")
    edad = (actual - fecha).days // 365 
    if edad < 16 : 
        return False

    dob = normalize_input(dob)
    return True 

# valido el usuario
def validate_user(user):
    valido = []
    valido.append(chr(46))
    for i in range(65,90):
        valido.append(chr(i))
    for i in range(97,122):
        valido.append(chr(i))

    for v in user:
        if v not in valido:
            return False

    user = normalize_input(user)
    return True


# valido el dni
def validate_dni(dni):
    dni_valid = int(dni)
    if not (1000000000 <= dni_valid <= 1999999999):
        return False
    return True




# valido la contraseña
def validate_pswd(pswd):
    if not (8 < len(pswd) < 35):
        return False

    valido_may = [chr(i) for i in range(65, 91)]
    valido_min = [chr(i) for i in range(97, 122)]
    valido_num = [str(i) for i in range(0,9)]
    num_car = [35,42,64,36,37,38,45,33,43,61,63]
    valido_car = [chr(i) for i in num_car]
    
    has_upper = has_lower = has_digit = has_special = False
    
    for i in pswd:
        if i in valido_may:
            has_upper = True
        elif i in valido_min:
            has_lower = True
        elif i in valido_num:
            has_digit = True
        elif i in valido_car:
            has_special = True
    
    if has_upper and has_lower and has_digit and has_special:
        return True
    else:
        return False



def validate_name(name):
    return True
