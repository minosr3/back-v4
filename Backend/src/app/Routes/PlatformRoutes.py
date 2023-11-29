from ..Models import Platform
from ..Services import PlatformDAO, Calculator
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..utils import db, loginManagerApp
from ..utils import Security


platformsMain = Blueprint('platformBlueprint', __name__)

@platformsMain.route('/platforms/', methods=['GET', 'POST'])
def handlePlatforms():
    try:
        print(request.method)
        if request.method == 'POST':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                result = PlatformDAO.createPlatform(data)
                if isinstance(result, Platform):  
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
        elif request.method == 'GET':
            platforms = PlatformDAO.getPlatforms()
            return jsonify(platforms), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@platformsMain.route('/platform/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handlePlatformById(id):
    hasAccess=Security.verifyToken(request.headers)
    if hasAccess:
        try:
            if request.method == 'GET':
                platform = PlatformDAO.getPlatformById(id)

                if platform is not None:
                    if isinstance(platform, Platform):
                        platformJSON = platform.to_JSON()
                        return jsonify(platformJSON), 200
                    else:
                        return jsonify({'message': str(ex)}), 500
                    
                else:
                    return jsonify({'message': 'Platform no encontrado'}), 404
            elif request.method == 'PUT':
                hasAccess = Security.verifyToken(request.headers, required_role=3)
                if hasAccess:
                    data = request.json
                    print(data)
                    platform = PlatformDAO.getPlatformById(id, data)
                    if platform is not None:
                        return jsonify({'message': 'Platform actualizado con éxito'}), 200
                    else:
                        return jsonify({'message': 'Platform no encontrado'}), 404
                else: 
                    return jsonify({'message': 'Unauthorized'}), 401
            elif request.method == 'DELETE':
                hasAccess = Security.verifyToken(request.headers, required_role=3)
                if hasAccess:
                    platform = PlatformDAO.getPlatformById(id)
                    if platform is not None:
                        # Llama a la función que elimina al platform
                        is_deleted = PlatformDAO.deletePlatform(id)
                        if is_deleted:
                            return jsonify({'message': 'Platform eliminado con éxito'}), 200
                        else:
                            return jsonify({'message': 'No se pudo eliminar al platform'}), 500
                    else:
                        return jsonify({'message': 'Platform no encontrado'}), 404
                else: 
                    return jsonify({'message': 'Unauthorized'}), 401
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401
