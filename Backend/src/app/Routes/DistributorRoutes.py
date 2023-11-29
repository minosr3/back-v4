from ..Models import Distributor
from ..Services import DistributorDAO, Calculator
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..utils import db, loginManagerApp
from ..utils import Security


distributorsMain = Blueprint('distributorBlueprint', __name__)

@distributorsMain.route('/distributors/', methods=['GET', 'POST'])
def handleDistributors():
    try:
        print(request.method)
        if request.method == 'POST':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                result = DistributorDAO.createDistributor(data)
                if isinstance(result, Distributor):  
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
            else:
                    return jsonify({'message': 'Unauthorized'}), 401
        elif request.method == 'GET':
            distributors = DistributorDAO.getDistributors()
            return jsonify(distributors), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@distributorsMain.route('/distributor/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleDistributorById(id):
    try:
        if request.method == 'GET':
            distributor = DistributorDAO.getDistributorById(id)

            if distributor is not None:
                if isinstance(distributor, Distributor):
                    distributorJSON = distributor.to_JSON()
                    return jsonify(distributorJSON), 200
                else:
                    return jsonify({'message': str(ex)}), 500
                
            else:
                return jsonify({'message': 'Distributor no encontrado'}), 404
        elif request.method == 'PUT':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                print(data)
                distributor = DistributorDAO.getDistributorById(id, data)
                if distributor is not None:
                    return jsonify({'message': 'Distributor actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'Distributor no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
        elif request.method == 'DELETE':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                distributor = DistributorDAO.getDistributorById(id)
                if distributor is not None:
                    # Llama a la función que elimina al distributor
                    is_deleted = DistributorDAO.deleteDistributor(id)
                    if is_deleted:
                        return jsonify({'message': 'Distributor eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al distributor'}), 500
                else:
                    return jsonify({'message': 'Distributor no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

