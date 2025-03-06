from _datetime import datetime
import time
from app.validation import *
from app.reading import *
from flask import request, jsonify, redirect, url_for, render_template, session, make_response
from app import app  # ✅ Usa la instancia de Flask de app/__init__.py
from app.encryption import *
from datetime import timedelta


# Configuración de sesiones
app.config['SESSION_TYPE'] = 'filesystem'  # Guarda sesiones en archivos
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True  # Protege contra manipulación de cookies
app.config['SESSION_FILE_DIR'] = './flask_sessions'  # Carpeta donde se guardarán las sesiones
app.config['SESSION_FILE_THRESHOLD'] = 100
app.config['SESSION_COOKIE_NAME'] = "session"
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # ⚠️ Debe ser True en producción si usas HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


login_attempts = {}
MAX_ATTEMPTS = 3
BLOCK_TIME = 300  # 5 minutos en segundos
app.secret_key = 'your_secret_key'
clave = b"e3b0c44298fc1c149afbf4c8996fb924"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True  # Permite actualizar la sesión con cada solicitud


def get_darkmode_preference():
    return request.cookies.get('darkmode', 'light')  

@app.before_request
def check_session_timeout():
    if request.endpoint is None:
        return
    allowed_routes = {'index','register','api_login', 'create_record', 'logout', 'static'}
    if 'email' in session:
        session.permanent = True  
        session.modified = True   
    elif request.endpoint not in allowed_routes:
        return redirect(url_for('api_login'))
    

@app.route('/api/users', methods=['POST'])
def create_record():
    data = request.form
    email = data.get('email')
    username = data.get('username')
    nombre = data.get('nombre')
    apellido = data.get('Apellidos')
    password = data.get('password')
    dni = data.get('dni')
    dob = data.get('dob')
    errores = []
    # Validaciones
    if not validate_email(email):
        errores.append("Email inválido")
    if not validate_pswd(password):
        errores.append("Contraseña inválida")
    if not validate_dob(dob):
        errores.append("Fecha de nacimiento inválida")
    if not validate_dni(dni):
        errores.append("DNI inválido")
    if not validate_user(username):
        errores.append("Usuario inválido")
    if not validate_name(nombre):
        errores.append("Nombre inválido")
    if not validate_name(apellido):
        errores.append("Apellido inválido")

    if errores:
        return render_template('form.html', error=errores)

    email = normalize_input(email)

    hashed_pwd, salt = hash_with_salt(normalize_input(password))

    dni_encrypt,nonce = encrypt_aes(dni,clave)

    db = read_db("db.txt")
    db[email] = {
        'nombre': normalize_input(nombre),
        'apellido': normalize_input(apellido),
        'username': normalize_input(username),
        'password': hashed_pwd,
        "password_salt": salt,
        "dni": dni_encrypt,
        'dob': normalize_input(dob),
        "role": "user",
        "nonce": nonce
    }

    write_db("db.txt", db)
    return redirect(url_for('login'))



# Endpoint para el login
@app.route('/api/login', methods=['GET', 'POST'])
def api_login():

    if request.method == 'GET':
        return render_template('login.html')
    
    email = normalize_input(request.form['email'])
    password = normalize_input(request.form['password'])

    db = read_db("db.txt")
    if email not in db:
        error = "Credenciales inválidas"
        return render_template('login.html', error=error)

    # Verificar si el usuario está bloqueado
    if email in login_attempts and login_attempts[email]['blocked_until'] > time.time():
        block_time_remaining = int((login_attempts[email]['blocked_until'] - time.time()) / 60)
        error = f"Cuenta bloqueada. Intenta nuevamente en {block_time_remaining} minutos."
        return render_template('login.html', error=error)

    password_db = db.get(email)["password"]
    salt_db = db.get(email)["password_salt"]

    # Validar si el correo existe en la base de datos
    if compare_salt(password, password_db, salt_db):
        # Resetear intentos fallidos
        login_attempts[email] = {'attempts': 0, 'blocked_until': 0}

        session['email'] = email
        session['role'] = db[email]['role']

        return redirect(url_for('customer_menu'))
    else:
        # Aumentar el contador de intentos fallidos
        if email not in login_attempts:
            login_attempts[email] = {'attempts': 0, 'blocked_until': 0}

        login_attempts[email]['attempts'] += 1

        # Bloquear la cuenta si se exceden los intentos
        if login_attempts[email]['attempts'] >= MAX_ATTEMPTS:
            login_attempts[email]['blocked_until'] = time.time() + BLOCK_TIME
            error = f"Se han excedido los intentos permitidos. Cuenta bloqueada por {BLOCK_TIME // 60} minutos."
        else:
            remaining_attempts = MAX_ATTEMPTS - login_attempts[email]['attempts']
            error = f"Credenciales incorrectas. Tienes {remaining_attempts} intentos restantes."

        return render_template('login.html', error=error)



# Página principal del menú del cliente
@app.route('/customer_menu')
def customer_menu():
    if 'email' not in session:
        error_msg = "Por favor, inicia sesión para acceder a esta página."
        return render_template('login.html', error=error_msg)
    
    if 'darkmode' not in session:
        session['darkmode'] = get_darkmode_preference()

    email = session.get('email')
    db = read_db("db.txt")
    transactions = read_db("transaction.txt")
    current_balance = sum(float(t['balance']) for t in transactions.get(email, []))
    last_transactions = transactions.get(email, [])[-5:]
    message = request.args.get('message', '')
    error = request.args.get('error', 'false').lower() == 'true'
    
    return render_template('customer_menu.html', message=message, nombre=db.get(email)['nombre'], balance=current_balance, last_transactions=last_transactions, error=error, darkmode=get_darkmode_preference())

# Endpoint para leer un registro
@app.route('/records', methods=['GET'])
def read_record():
    if 'email' not in session:
        error_msg = "Por favor, inicia sesión para acceder a esta página."
        return render_template('login.html', error=error_msg, darkmode=get_darkmode_preference())

    db = read_db("db.txt")
    user_email = session.get('email')
    user = db.get(user_email, None)

    db_copia = db.copy()

    for email, data in db_copia.items():
        dni = data.get("dni")
        nonce = data.get("nonce")
        if dni and nonce:
            dni_of = cuatro_digitos(dni, nonce, clave)
            db_copia[email]["dni"] = dni_of

    user_copia = db_copia.get(user_email, None)
    message = request.args.get('message', '')

    darkmode = request.cookies.get('darkmode', 'light')
    session['darkmode'] = darkmode  

    if session.get('role') == 'admin':
        return render_template('records.html', users=db_copia, role=session.get('role'), message=message, darkmode=darkmode)
    else:
        return render_template('records.html', users={user_email: user_copia}, error=None, message=message, darkmode=darkmode)


@app.route('/update_user/<email>', methods=['POST'])
def update_user(email):
    if 'email' not in session:
        # Redirigir a la página de inicio de sesión si el usuario no está autenticado
        error_msg = "Por favor, inicia sesión para acceder a esta página."
        return render_template('login.html', error=error_msg)
    # Leer la base de datos de usuarios
    db = read_db("db.txt")

    username = request.form['username']
    dni = request.form['dni']
    dob = request.form['dob']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    darkmode = 'dark' if request.form.get('darkmode') == 'on' else 'light'
    
    
    errores = []

    if not validate_dob(dob):
        errores.append("Fecha de nacimiento inválida")
    if not validate_dni(dni):
        errores.append("DNI inválido")
    if not validate_user(username):
        errores.append("Usuario inválido")
    if not validate_name(nombre):
        errores.append("Nombre inválido")
    if not validate_name(apellido):
        errores.append("Apellido inválido")

    if errores:
        return render_template('edit_user.html',
                               user_data=db[email],
                               email=email,
                               error=errores)

    dni_encrypt,nonce = encrypt_aes(dni,clave)

    db[email]['username'] = normalize_input(username)
    db[email]['nombre'] = normalize_input(nombre)
    db[email]['apellido'] = normalize_input(apellido)
    db[email]['dni'] = dni_encrypt
    db[email]['nonce'] = nonce
    db[email]['dob'] = normalize_input(dob)


    write_db("db.txt", db)
    resp = make_response(redirect(url_for('read_record', message="Información actualizada correctamente")))
    resp.set_cookie('darkmode', darkmode, max_age=30*24*60*60, secure=True, httponly=False, samesite='Lax')

    # Redirigir al usuario a la página de records con un mensaje de éxito
    return resp

@app.route('/api/delete_user/<email>', methods=['GET'])
def delete_user(email):
    if 'email' not in session:
        # Redirigir a la página de inicio de sesión si el usuario no está autenticado
        error_msg = "Por favor, inicia sesión para acceder a esta página."
        return render_template('login.html', error=error_msg)
    
    if session.get('role') == 'admin':
        db = read_db("db.txt")

        if email not in db:
            return redirect(url_for('read_record', message="Usuario no encontrado"))

        if session.get('email') == email:
            session.clear()

        del db[email] 

        write_db("db.txt", db)

        return redirect(url_for('read_record', message="Usuario eliminado correctamente"))
    else:
        return redirect(url_for('read_record', message="No autorizado"))


# Endpoint para depósito
@app.route('/api/deposit', methods=['POST'])
def api_deposit():
    if 'email' not in session:
        # Redirigir a la página de inicio de sesión si el usuario no está autenticado
        error_msg = "Por favor, inicia sesión para acceder a esta página."
        return render_template('login.html', error=error_msg)

    deposit_balance = request.form['balance']
    deposit_email = session.get('email')

    db = read_db("db.txt")
    transactions = read_db("transaction.txt")

    if 'darkmode' not in session:
        session['darkmode'] = get_darkmode_preference()
    
    # Verificamos si el usuario existe
    if deposit_email in db:
        # Guardamos la transacción
        transaction = {"balance": deposit_balance, "type": "Deposit", "timestamp": str(datetime.now())}

        # Verificamos si el usuario tiene transacciones previas
        if deposit_email in transactions:
            transactions[deposit_email].append(transaction)
        else:
            transactions[deposit_email] = [transaction]
        write_db("transaction.txt", transactions)

        return redirect(url_for('customer_menu', message="Depósito exitoso",darkmode=get_darkmode_preference()))

    return redirect(url_for('customer_menu', message="Email no encontrado",darkmode=get_darkmode_preference()))


# Endpoint para retiro
@app.route('/api/withdraw', methods=['POST'])
def api_withdraw():
    if 'email' not in session:
        # Redirigir a la página de inicio de sesión si el usuario no está autenticado
        error_msg = "Por favor, inicia sesión para acceder a esta página."
        return render_template('login.html', error=error_msg)
    db = read_db("db.txt")
    email = session.get('email')
    amount = float(request.form['balance'])
    password = normalize_input(request.form['password'])
    if amount <= 0:
        return redirect(url_for('customer_menu',
                                message="La cantidad a retirar debe ser positiva",
                                error=True),
                                darkmode=get_darkmode_preference())

    transactions = read_db("transaction.txt")
    current_balance = sum(float(t['balance']) for t in transactions.get(email, []))

    password_db = db.get(email)["password"]
    salt_db = db.get(email)["password_salt"]
    igual = compare_salt(password, password_db, salt_db)
    if igual:
        if amount > current_balance:
            return redirect(url_for('customer_menu',
                                message="Saldo insuficiente para retiro",
                                error=True))
        transaction = {"balance": -amount, "type": "Withdrawal", "timestamp": str(datetime.now())}

        if email in transactions:
            transactions[email].append(transaction)
        else:
            transactions[email] = [transaction]

        write_db("transaction.txt", transactions)

        return redirect(url_for('customer_menu',
                            message="Retiro exitoso",
                            error=False),
                            darkmode=get_darkmode_preference())
    else:
        return redirect(url_for('customer_menu', message="Retiro no autorizado: Contraseña incorrecta"),darkmode=get_darkmode_preference())
    
