from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..Models import User, UserVO
from ..Services import UserDAO
from ..utils import Security

userMain = Blueprint('userBlueprint', __name__)

@userMain.route('/')
def index():
    return "Hello, Mr. Sun! La tierra les dice hola"

@userMain.route('/users/', methods=['GET', 'POST'])
def handleUsers():
    hasAccess=Security.verifyToken(request.headers)
    if hasAccess: 
        try:
            if request.method == 'POST':
                data = request.json
                result = UserDAO.createUser(data)
                if isinstance(result, User):  
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
            elif request.method == 'GET':
                users = UserDAO.getUsers()
                usersdetails_json = []
                for user in users:
                    userJSON = user.to_JSON()
                    countryJson, rolJson, payModeJson = UserDAO.getDetailsToUser(user)
                    usersdetails_json.append({
                        'user': userJSON,
                        'country': countryJson,
                        'rol': rolJson,
                        'payMode': payModeJson
                    }) 
                return jsonify(usersdetails_json), 200
            return render_template('auth/create.html')
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401


@userMain.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleUserById(id):
    hasAccess=Security.verifyToken(request.headers)
    if hasAccess: 
        try:
            if request.method == 'GET':
                user = UserDAO.getUserByID(id)
                if user is not None:
                    if isinstance(user, User):
                        userJSON = user.to_JSON()
                        countryJson, rolJson, payModeJson = UserDAO.getDetailsToUser(user)
                        userdetails_json = ({
                            'user': userJSON,
                            'country': countryJson,
                            'rol': rolJson,
                            'payMode': payModeJson
                        })
                        return jsonify(userdetails_json), 200
                    else:
                        return jsonify({'message': str(ex)}), 500
                    
                else:
                    return jsonify({'message': 'Usuario no encontrado'}), 404
            elif request.method == 'PUT':
                data = request.json
                print(data)
                user = UserDAO.uptadeUser(id, data)
                if user is not None:
                    return jsonify({'message': 'Usuario actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'Usuario no encontrado'}), 404
            elif request.method == 'DELETE':
                user = UserDAO.getUserByID(id)
                if user is not None:
                    is_deleted = UserDAO.deleteUser(id)
                    if is_deleted:
                        return jsonify({'message': 'Usuario eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al usuario'}), 500
                else:
                    return jsonify({'message': 'Usuario no encontrado'}), 404
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401

@userMain.route('/users/<string:email>', methods=['GET', 'PUT', 'DELETE'])
def handleUserByEmail(email):
    hasAccess=Security.verifyToken(request.headers)
    if hasAccess:
        try:
            if request.method == 'GET':
                user = UserDAO.getUserByEmail(email)
                if user is not None:

                    user_json = user.to_JSON()
                    countryJson, rolJson, payModeJson = UserDAO.getDetailsToUser(user)

                    userDetails_json = {
                        'user': user_json,
                        'country': countryJson,
                        'rol': rolJson,
                        'payMode': payModeJson
                    }
                    return jsonify(userDetails_json), 200
                else:
                    return jsonify({'message': 'Usuario no encontrado'}), 404
            elif request.method == 'PUT':
                return jsonify({'message': 'Funcion no habilitada'}), 501
            elif request.method == 'DELETE':
                return jsonify({'message': 'Funcion no habilitada'}), 501

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401
    
    
