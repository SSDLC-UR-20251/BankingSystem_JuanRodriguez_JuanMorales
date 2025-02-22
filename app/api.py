from _datetime import datetime
import time
from app.validation import *
from app.reading import *
from flask import request, jsonify, redirect, url_for, render_template, session, make_response, flash
from app import app
from functools import wraps

app.secret_key = 'your_secret_key'

MAX_INTENTOS = 3
TIEMPO_BLOQUEO = 5 * 60  # 5 minutos en segundos

# Diccionario para gestionar intentos y bloqueos en memoria
usuarios_intentos = {}

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
    role = data.get('role', 'user')  # Por defecto, los usuarios serán 'user'
    errores = []
    print(data)
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
   

    db = read_db("db.txt")

     # Solo permitir que un admin asigne roles
    if 'role' in session and session['role'] == 'admin':
        assigned_role = role if role in ['admin', 'user'] else 'user'
    else:
        assigned_role = 'user'  # Usuarios normales no pueden asignar roles

    db[email] = {
        'nombre': normalize_input(nombre),
        'apellido': normalize_input(apellido),
        'username': normalize_input(username),
        'password': normalize_input(password),
        "dni": dni,
        'dob': normalize_input(dob),
        "role":"admin"
    }

    write_db("db.txt", db)
    return redirect("/login")


# Endpoint para el login
@app.route('/api/login', methods=['POST'])
def api_login():
    email = normalize_input(request.form['email'])
    password = normalize_input(request.form['password'])
    db = read_db("db.txt")

    if email not in db:
        error = "Credenciales inválidas"
        return render_template('login.html', error=error)

    ahora = time.time()
    if email in usuarios_intentos and usuarios_intentos[email]["bloqueo"] > ahora:
        return render_template('login.html', error="Usuario bloqueado. Inténtelo más tarde.")
    
    password_db = db.get(email)["password"]

    if password_db == password :
        session['email'] = email
        session['role'] = db[email].get('role', 'user')
        usuarios_intentos.pop(email, None)  
        return redirect(url_for('customer_menu'))

    if email not in usuarios_intentos:
        usuarios_intentos[email] = {"intentos": 0, "bloqueo": 0}
    
    usuarios_intentos[email]["intentos"] += 1

    if usuarios_intentos[email]["intentos"] >= MAX_INTENTOS:
        usuarios_intentos[email]["bloqueo"] = ahora + TIEMPO_BLOQUEO
        return render_template('login.html', error=f"Usuario bloqueado por {TIEMPO_BLOQUEO//60} minutos.")
    
    return render_template('login.html', error=f"Intento fallido {usuarios_intentos[email]['intentos']}/{MAX_INTENTOS}")


# Página principal del menú del cliente
@app.route('/customer_menu')
def customer_menu():

    db = read_db("db.txt")

    transactions = read_db("transaction.txt")
    current_balance = 100
    last_transactions = []
    message = request.args.get('message', '')
    error = request.args.get('error', 'false').lower() == 'true'
    return render_template('customer_menu.html',
                           message=message,
                           nombre="",
                           balance=current_balance,
                           last_transactions=last_transactions,
                           error=error,)


# Endpoint para leer un registro
@app.route('/records', methods=['GET'])
def read_record():
    db = read_db("db.txt")
    message = request.args.get('message', '')
    return render_template('records.html', users=db,role=session.get('role'),message=message)


@app.route('/update_user/<email>', methods=['POST'])
def update_user(email):
    # Leer la base de datos de usuarios
    db = read_db("db.txt")

    username = request.form['username']
    dni = request.form['dni']
    dob = request.form['dob']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
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


    db[email]['username'] = normalize_input(username)
    db[email]['nombre'] = normalize_input(nombre)
    db[email]['apellido'] = normalize_input(apellido)
    db[email]['dni'] = dni
    db[email]['dob'] = normalize_input(dob)


    write_db("db.txt", db)
    

    # Redirigir al usuario a la página de records con un mensaje de éxito
    return redirect(url_for('read_record', message="Información actualizada correctamente"))

def admin_required(f):

    @wraps(f)
    def wrapped(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("No tienes permisos para acceder a esta página.", "danger")
            return redirect(url_for('customer_menu'))
        return f(*args, **kwargs)
    return wrapped

@app.route('/records', methods=['GET'])
def read_record():
    db = read_db("db.txt")
    message = request.args.get('message', '')

    # Si el usuario es admin, ve todos los registros
    if session.get('role') == 'admin':
        return render_template('records.html', users=db, role='admin', message=message)

    # Si es usuario normal, solo ve su propio registro
    email = session.get('email')
    if email in db:
        return render_template('records.html', users={email: db[email]}, role='user', message=message)

    return redirect(url_for('customer_menu'))

@app.route('/delete_user/<email>', methods=['POST'])
@admin_required  # Solo un admin puede eliminar usuarios
def delete_user(email):
    db = read_db("db.txt")

    if email in db:
        del db[email]
        write_db("db.txt", db)
        flash("✅ Usuario eliminado con éxito.", "success")

    return redirect(url_for('read_record'))