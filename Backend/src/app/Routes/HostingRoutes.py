from ..Models import Hosting
from ..Services import HostingDAO, Verifications
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from ..utils import db, loginManagerApp
from ..utils import Security

hostingsMain = Blueprint('hostingBlueprint', __name__)

@hostingsMain.route('/hostings/<int:id>', methods=['GET', 'POST'])
@hostingsMain.route('/hostings/', defaults={'id': 0}, methods=['GET', 'POST'])
def handleHostings(id = 0):
    hasAccess = Security.verifyToken(request.headers)
    if hasAccess:
        try:
            print(request.method)
            if request.method == 'POST':
                data = request.json
                result = HostingDAO.createHosting(data, id)
                if isinstance(result, Hosting):  
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
            elif request.method == 'GET':
                hostings = Verifications.getHostingsOfCurrentUser(id)
                if hostings is None:
                    hostings = HostingDAO.getHostings()
                totalInfoHostings = []
                for hosting in hostings:
                    hostingJSON = hosting.to_JSON()
                    hostingPlan = HostingDAO.getHostingPlan(hosting)
                    planJSON = hostingPlan.to_JSON()
                    totalInfoHostings.append({
                        'hosting': hostingJSON,
                        'hostingPlan': planJSON
                    })
                return jsonify(totalInfoHostings), 200
        except Exception as ex:
            return jsonify({'message': f'Error interno: {str(ex)}'}), 500
    else:
        return jsonify({'message': 'No autorizado'}), 401

@hostingsMain.route('/hosting/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleHostingById(id):
    hasAccess=Security.verifyToken(request.headers)
    if hasAccess:
        try:
            if request.method == 'GET':
                hosting = HostingDAO.getHostingById(id)
                if hosting is not None:
                    if isinstance(hosting, Hosting):
                        hostingJSON = hosting.to_JSON()
                        hostingPlan = HostingDAO.getHostingPlan(hosting)
                        planJSON = hostingPlan.to_JSON()
                        totalInfoHostings = ({
                            'hosting': hostingJSON,
                            'hostingPlan': planJSON
                        })
                        return jsonify(totalInfoHostings), 200
                    else:
                        return jsonify({'message': str(ex)}), 500
                    
                else:
                    return jsonify({'message': 'Hosting no encontrado'}), 404
            elif request.method == 'PUT':
                data = request.json
                print(data)
                hosting = HostingDAO.updateHosting(id, data)
                if hosting is not None:
                    return jsonify({'message': 'Hosting actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'Hosting no encontrado'}), 404
            elif request.method == 'DELETE':
                hosting = HostingDAO.getHostingById(id)
                if hosting is not None:
                    is_deleted = HostingDAO.deleteHosting(id)
                    if is_deleted:
                        return jsonify({'message': 'Hosting eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al hosting'}), 500
                else:
                    return jsonify({'message': 'Hosting no encontrado'}), 404
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401

@hostingsMain.before_request
def before_request():
    # Recargar el usuario en cada solicitud
    if current_user.is_authenticated:
        print("Usuario autenticado")