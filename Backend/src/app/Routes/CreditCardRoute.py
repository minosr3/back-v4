from ..Models import CreditCard
from ..Services import CreditCardDAO, Calculator, Verifications
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..utils import db, loginManagerApp
from ..utils import Security

creditCardsMain = Blueprint('creditCardBlueprint', __name__)

@creditCardsMain.route('/creditCards/<int:id>', methods=['GET', 'POST'])
@creditCardsMain.route('/creditCards/', defaults={'id': 0}, methods=['GET', 'POST'])
def handleCreditCards(id = 0):
    hasAccess = Security.verifyToken(request.headers, required_role=1)
    hasAccess = True
    if hasAccess:    
        try:
            if request.method == 'POST':
                data = request.json
                result = CreditCard
                result = CreditCardDAO.createCreditCard(data)

                if isinstance(result, CreditCard): 
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                elif 'error' in result:
                    return jsonify({'error': result['error']}), 400
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
            elif request.method == 'GET':
                creditCards = Verifications.get_itemsOfCurrentUser(id, 'CreditCard')
                if creditCards is not None:
                    totalInfoCreditCards = []
                    for creditCard in creditCards:
                        creditCardJSON = creditCard.to_JSON()
                        totalInfoCreditCards.append(creditCardJSON)
                    return jsonify(totalInfoCreditCards), 200
                else: 
                    return jsonify({'message': 'Not found'}), 404
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401


@creditCardsMain.route('/creditCard/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleCreditCardById(id):
    hasAccess = Security.verifyToken(request.headers)
    if hasAccess:
        try:
            if request.method == 'GET':
                creditCard = CreditCardDAO.getCreditCardById(id)
                if creditCard is not None:
                    if isinstance(creditCard, CreditCard):
                        creditCardJSON = creditCard.to_JSON()
                        return jsonify(creditCard), 200
                    else:
                        return jsonify({'message': 'error'}), 500
                else:
                    return jsonify({'message': 'CreditCard no encontrado'}), 404
            elif request.method == 'PUT':
                data = request.json
                print(data)
                creditCard = CreditCardDAO.updateCreditCard(id, data)
                if creditCard is not None:
                    return jsonify({'message': 'CreditCard actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'CreditCard no encontrado'}), 404
            elif request.method == 'DELETE':
                creditCard = CreditCardDAO.getCreditCardById(id)
                if creditCard is not None:
                    is_deleted = CreditCardDAO.deleteCreditCard(id)
                    if is_deleted:
                        return jsonify({'message': 'CreditCard eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al creditCard'}), 500
                else:
                    return jsonify({'message': 'CreditCard no encontrado'}), 404
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401

