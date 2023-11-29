from ..Models import PayPlan
from ..Services import PayPlanDAO, Calculator
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..utils import db, loginManagerApp
from ..utils import Security


payPlansMain = Blueprint('payPlanBlueprint', __name__)

@payPlansMain.route('/payPlans/', methods=['GET', 'POST'])
def handlePayPlans():
    try:
        print(request.method)
        if request.method == 'POST':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                result = PayPlanDAO.createPayPlan(data)
                if isinstance(result, PayPlan):  
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
        elif request.method == 'GET':
            payPlans = PayPlanDAO.getPayPlans()
            return jsonify(payPlans), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@payPlansMain.route('/payPlan/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handlePayPlanById(id):
    try:
        if request.method == 'GET':
            payPlan = PayPlanDAO.getPayPlanById(id)

            if payPlan is not None:
                if isinstance(payPlan, PayPlan):
                    payPlanJSON = payPlan.to_JSON()
                    return jsonify(payPlanJSON), 200
                else:
                    return jsonify({'message': str(ex)}), 500
                
            else:
                return jsonify({'message': 'PayPlan no encontrado'}), 404
        elif request.method == 'PUT':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                print(data)
                payPlan = PayPlanDAO.getPayPlanById(id, data)
                if payPlan is not None:
                    return jsonify({'message': 'PayPlan actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'PayPlan no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
        elif request.method == 'DELETE':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                payPlan = PayPlanDAO.getPayPlanById(id)
                if payPlan is not None:
                    # Llama a la función que elimina al payPlan
                    is_deleted = PayPlanDAO.deletePayPlan(id)
                    if is_deleted:
                        return jsonify({'message': 'PayPlan eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al payPlan'}), 500
                else:
                    return jsonify({'message': 'PayPlan no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
