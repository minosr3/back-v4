from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..Models import User
from ..Services import UserDAO
from ..Services import LoginService
from ..utils import loginManagerApp, Security
from flask_login import login_user, logout_user, login_required, current_user

authMain = Blueprint('authBlueprint', __name__)

def status401(error):
    return redirect(url_for('authBlueprint.login'))

def status404(error): 
    return "<h1>404<br>Not found page :(</h1>", 404

@authMain.route('/home/')
def home():
    print("ya en el home, bienvenido")
    if isinstance(current_user, User):
        print(current_user.is_authenticated)
    else:
        print("current_user is not a User object")
    
    return render_template('home.html')

@authMain.route('/ver/')
def verification():
    if current_user.is_authenticated:
        return f"Página de inicio. Usuario autenticado: {current_user.id}"
    else:
        return "Página de inicio. No hay usuario autenticado."

@loginManagerApp.user_loader
def loadUser(id):
    user = UserDAO.getUserByID(id)
    return user

@authMain.route('/create/', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        # Captura los datos del formulario
        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')
        idDocument = request.json.get('idDocument')
        document_type = request.json.get('document_type')
        phone = request.json.get('phone')
        country_id = request.json.get('country_id')

        print("Nombre:", name)
        print("Correo electrónico:", email)
        print("Contraseña:", password)
        print("Número de identificación:", idDocument)
        print("Tipo de identificación:", document_type)


        # Crea un arreglo para almacenar los datos
        data = []

        # Agrega los datos del formulario al arreglo
        data = {
            'name': name,
            'password': password,
            'email': email,
            'idDocument': idDocument,
            'document_type': document_type,
            'phone':phone,
            'country_id':country_id
        }


        # Aquí puedes procesar los datos, por ejemplo, guardarlos en una base de datos
        # o realizar cualquier otra acción necesaria.
        print(data)
        result = UserDAO.createUser(data)
        if isinstance(result, User):  
            return jsonify({'message': 'Operación POST exitosa'}), 201
        else:
            return jsonify({'message': 'Error desconocido'}), 500
    elif request.method == 'GET':
        return jsonify({'message': 'Method Not Allowed'}), 405  
    

@authMain.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #csrfToken = request.form.get('csrf_token')
        #print(csrfToken)
        email = request.json.get('email')  
        password = request.json.get('password') 
        print(email)
        print(password)
        loggedUser = LoginService.login(email, password)
        if loggedUser is not None:
            if loggedUser.password is True:
                login_user(loggedUser, remember=True)
                encodedToken = Security.generateToken(loggedUser)
                print(encodedToken)
                print("Contraseña correcta, usuario autenticado")
                #loginManagerApp._set_cookie(loggedUser)
                #session.set_permanent("current_user", user)
                return jsonify({'mensaje': 'Inicio de sesión exitoso', 'Token':encodedToken, 'Name':current_user.name, 'Rol':current_user.rol_id, 'id':current_user.id}), 200
            else: 
                flash("Contraseña incorrecta, no se pudo autenticar")
                print("Contraseña incorrecta, no se pudo autenticar")
                return redirect(url_for("authBlueprint.home"))
                #return jsonify({'mensaje': 'Error de autenticación: contraseña incorrecta'}), 401
                
        else:
            flash("Usuario no encontrado...")
            print("El usuario no existe")
            #return jsonify({'message': 'Usuario no encontrado'}), 404
        
        return render_template('auth/login.html')
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405

@authMain.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authBlueprint.login'))

@authMain.route('/protected/')
@login_required
def protected():
    return "<h1>Esta en una vista protegida, unicamente para usuarios autenticados</h1>"

#Funcion de prueba para mirar el tema del login 
@authMain.route('/userslogin/', methods=['GET', 'POST'])
def loginInUser():
    if request.method == 'POST':
        email = request.json.get('email')  
        password = request.json.get('password')
        print(email)
        print(password)
        loggedUser = LoginService.login(email, password)
        if loggedUser is not None:
            if loggedUser.password is True:
                encodedToken = Security.generateToken(loggedUser)
                return jsonify({'mensaje': 'Inicio de sesión exitoso', 'Token':encodedToken}), 200
            else: 
                return jsonify({'mensaje': 'Error de autenticación: contraseña incorrecta'}), 401
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    else:
        return jsonify({'message': 'Method Not Allowed'}), 405
    