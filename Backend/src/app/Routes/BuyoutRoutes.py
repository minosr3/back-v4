from ..Models import Buyout
from ..Services import BuyoutDAO, Calculator, Verifications
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..utils import db, loginManagerApp
from ..utils import Security

buyoutsMain = Blueprint('buyoutBlueprint', __name__)

@buyoutsMain.route('/buyouts/<int:id>', methods=['GET', 'POST'])
@buyoutsMain.route('/buyouts/', defaults={'id': 0}, methods=['GET', 'POST'])
def handleBuyouts(id = 0):
    hasAccess = Security.verifyToken(request.headers, required_role=1)
    hasAccess = True
    if hasAccess:    
        try:
            if request.method == 'POST':
                data = request.json
                result = BuyoutDAO.createBuyout(data)

                if isinstance(result, Buyout): 
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                elif 'error' in result:
                    return jsonify({'error': result['error']}), 400
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
            elif request.method == 'GET':
                buyouts = Verifications.get_itemsOfCurrentUser(id, 'Buyout')
                if buyouts is None:
                    buyouts = BuyoutDAO.getBuyouts()
                totalInfoBuyouts = []
                for buyout in buyouts:
                    buyoutJSON = buyout.to_JSON()
                    Domains = BuyoutDAO.getBuyoutsDomains(buyout)
                    Hostings = BuyoutDAO.getBuyoutsHostings(buyout)
                    buyoutDomains = [domain.to_JSON() for domain in Domains]
                    buyoutHostings = [hosting.to_JSON() for hosting in Hostings]
                    costDomains = Calculator.calcular_precioFinalDomains(Domains)
                    costHostings = Calculator.calcular_precioFinalHostings(Hostings)
                    totalCost = costDomains + costHostings
                    totalInfoBuyouts.append({
                        'buyouts': buyoutJSON,
                        'buyoutsDomains': buyoutDomains,
                        'buyoutsHosting': buyoutHostings,
                        'costDomains': costDomains,
                        'costHostings': costHostings,
                        'totalCost':totalCost
                    })
                return jsonify(totalInfoBuyouts), 200
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401


@buyoutsMain.route('/buyout/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleBuyoutById(id):
    hasAccess = Security.verifyToken(request.headers)
    if hasAccess:
        try:
            if request.method == 'GET':
                buyout = BuyoutDAO.getBuyoutById(id)
                if buyout is not None:
                    if isinstance(buyout, Buyout):
                        buyoutJSON = buyout.to_JSON()
                        Domains = BuyoutDAO.getBuyoutsDomains(buyout)
                        Hostings = BuyoutDAO.getBuyoutsHostings(buyout)
                        buyoutDomains = [domain.to_JSON() for domain in Domains]
                        buyoutHostings = [hosting.to_JSON() for hosting in Hostings]
                        costDomains = Calculator.calcular_precioFinalDomains(Domains)
                        costHostings = Calculator.calcular_precioFinalHostings(Hostings)
                        totalCost = costDomains + costHostings
                        totalInfoBuyouts = {
                            'buyouts': buyoutJSON,
                            'buyoutsDomains': buyoutDomains,
                            'buyoutsHosting': buyoutHostings,
                            'costDomains': costDomains,
                            'costHostings': costHostings,
                            'totalCost':totalCost
                        }
                        return jsonify(totalInfoBuyouts), 200
                    else:
                        return jsonify({'message': 'error'}), 500
                else:
                    return jsonify({'message': 'Buyout no encontrado'}), 404
            elif request.method == 'PUT':
                data = request.json
                print(data)
                buyout = BuyoutDAO.updateBuyout(id, data)
                if buyout is not None:
                    return jsonify({'message': 'Buyout actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'Buyout no encontrado'}), 404
            elif request.method == 'DELETE':
                buyout = BuyoutDAO.getBuyoutById(id)
                if buyout is not None:
                    is_deleted = BuyoutDAO.deleteBuyout(id)
                    if is_deleted:
                        return jsonify({'message': 'Buyout eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al buyout'}), 500
                else:
                    return jsonify({'message': 'Buyout no encontrado'}), 404
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401

