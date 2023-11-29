from ..Models import Plan
from ..Services import PlanDAO, Calculator
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..utils import db, loginManagerApp
from ..utils import Security


plansMain = Blueprint('planBlueprint', __name__)

@plansMain.route('/plans/', methods=['GET', 'POST'])
def handlePlans():
    try:
        print(request.method)
        if request.method == 'POST':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                result = PlanDAO.createPlan(data)
                if isinstance(result, Plan):  
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
        elif request.method == 'GET':
            plans = PlanDAO.getPlans()
            return jsonify(plans), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@plansMain.route('/plan/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handlePlanById(id):
    try:
        if request.method == 'GET':
            plan = PlanDAO.getPlanById(id)

            if plan is not None:
                if isinstance(plan, Plan):
                    planJSON = plan.to_JSON()
                    return jsonify(planJSON), 200
                else:
                    return jsonify({'message': str(ex)}), 500
                
            else:
                return jsonify({'message': 'Plan no encontrado'}), 404
        elif request.method == 'PUT':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                print(data)
                plan = PlanDAO.getPlanById(id, data)
                if plan is not None:
                    return jsonify({'message': 'Plan actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'Plan no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
        elif request.method == 'DELETE':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                plan = PlanDAO.getPlanById(id)
                if plan is not None:
                    is_deleted = PlanDAO.deletePlan(id)
                    if is_deleted:
                        return jsonify({'message': 'Plan eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al plan'}), 500
                else:
                    return jsonify({'message': 'Plan no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
