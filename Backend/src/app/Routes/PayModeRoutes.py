from ..Models import PayMode
from ..Services import PayModeDAO, Calculator
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..utils import db, loginManagerApp
from ..utils import Security


payModesMain = Blueprint('payModeBlueprint', __name__)

@payModesMain.route('/payModes/', methods=['GET', 'POST'])
def handlePayModes():
    try:
        print(request.method)
        if request.method == 'POST':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                result = PayModeDAO.createPayMode(data)
                if isinstance(result, PayMode):  
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
        elif request.method == 'GET':
            payModes = PayModeDAO.getPayModes()
            return jsonify(payModes), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@payModesMain.route('/payMode/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handlePayModeById(id):
    try:
        if request.method == 'GET':
            payMode = PayModeDAO.getPayModeById(id)

            if payMode is not None:
                if isinstance(payMode, PayMode):
                    payModeJSON = payMode.to_JSON()
                    return jsonify(payModeJSON), 200
                else:
                    return jsonify({'message': str(ex)}), 500
                
            else:
                return jsonify({'message': 'PayMode no encontrado'}), 404
        elif request.method == 'PUT':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                print(data)
                payMode = PayModeDAO.getPayModeById(id, data)
                if payMode is not None:
                    return jsonify({'message': 'PayMode actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'PayMode no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
        elif request.method == 'DELETE':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                payMode = PayModeDAO.getPayModeById(id)
                if payMode is not None:
                    # Llama a la función que elimina al payMode
                    is_deleted = PayModeDAO.deletePayMode(id)
                    if is_deleted:
                        return jsonify({'message': 'PayMode eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al payMode'}), 500
                else:
                    return jsonify({'message': 'PayMode no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
