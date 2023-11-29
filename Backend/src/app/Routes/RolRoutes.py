from ..Models import Rol
from ..Services import RolDAO
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..utils import db, loginManagerApp
from ..utils import Security


rolsMain = Blueprint('rolBlueprint', __name__)

@rolsMain.route('/rols/', methods=['GET', 'POST'])
def handleRols():
        try:
            print(request.method)
            if request.method == 'POST':
                hasAccess = Security.verifyToken(request.headers, required_role=3)
                if hasAccess:
                    data = request.json
                    result = RolDAO.createRol(data)
                    if isinstance(result, Rol):  
                        return jsonify({'message': 'Operación POST exitosa'}), 201
                    else:
                        return jsonify({'message': 'Error desconocido'}), 500
            elif request.method == 'GET':
                rols = RolDAO.getRols()
                return jsonify(rols), 200
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500


@rolsMain.route('/rol/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleRolById(id):
    try:
        if request.method == 'GET':
            rol = RolDAO.getRolById(id)

            if rol is not None:
                if isinstance(rol, Rol):
                    rolJSON = rol.to_JSON()
                    return jsonify(rolJSON), 200
                else:
                    return jsonify({'message': str(ex)}), 500
                
            else:
                return jsonify({'message': 'Rol no encontrado'}), 404
        elif request.method == 'PUT':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                print(data)
                rol = RolDAO.getRolById(id, data)
                if rol is not None:
                    return jsonify({'message': 'Rol actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'Rol no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
        elif request.method == 'DELETE':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                rol = RolDAO.getRolById(id)
                if rol is not None:
                    # Llama a la función que elimina al rol
                    is_deleted = RolDAO.deleteRol(id)
                    if is_deleted:
                        return jsonify({'message': 'Rol eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al rol'}), 500
                else:
                    return jsonify({'message': 'Rol no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
