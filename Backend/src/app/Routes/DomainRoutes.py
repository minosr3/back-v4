from ..Models import Domain, Distributor
from ..Services import DomainDAO, Calculator, Verifications
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from ..utils import db, loginManagerApp
from ..utils import Security


domainsMain = Blueprint('domainBlueprint', __name__)

@domainsMain.route('/domains/<int:id>', methods=['GET', 'POST'])
@domainsMain.route('/domains/', defaults={'id': 0}, methods=['GET', 'POST'])
def handleDomainsWithUser(id = 0):
    try:
        print(request.method)
        if request.method == 'POST':
            hasAccess=Security.verifyToken(request.headers)
            hasAccess = True
            if hasAccess:
                data = request.json
                print(data)
                result = DomainDAO.createDomain(data, id)

                if isinstance(result, Domain):  
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
        elif request.method == 'GET':
            domains = Verifications.getDomainsOfCurrentUser(id)
            if domains is None:
                domains = DomainDAO.getDomains()
            totalInfoDomains = []
            for domain in domains:
                domainJson = domain.to_JSON()
                Distributor = DomainDAO.getDomainsDistributors(domain)
                domainDistributor = Distributor.to_JSON()
                commission = Calculator.calcular_comision(domain)
                totalInfoDomains.append({
                    'domain' : domainJson,
                    'domainDistributor' : domainDistributor,
                    'commission' : commission 
                })
            return jsonify(totalInfoDomains), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500   


@domainsMain.route('/domain/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleDomainById(id):
    hasAccess=Security.verifyToken(request.headers)
    if hasAccess:
        try:
            if request.method == 'GET':
                domain = DomainDAO.getDomainById(id)
                if domain is not None:
                    if isinstance(domain, Domain):
                        domainJson = domain.to_JSON()
                        Distributor = DomainDAO.getDomainsDistributors(domain)
                        domainDistributor = Distributor.to_JSON()
                        commission = Calculator.calcular_comision(domain)
                        totalInfoDomains = {
                            'domain' : domainJson,
                            'domainDistributor' : domainDistributor,
                            'commission' : commission 
                        }
                        return jsonify(totalInfoDomains), 200
                    else:
                        return jsonify({'message': str(ex)}), 500
                    
                else:
                    return jsonify({'message': 'Domain no encontrado'}), 404
            elif request.method == 'PUT':
                data = request.json
                print(data)
                domain = DomainDAO.updateDomain(id, data)
                if domain is not None:
                    return jsonify({'message': 'Domain actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'Domain no encontrado'}), 404
            elif request.method == 'DELETE':
                domain = DomainDAO.getDomainById(id)
                if domain is not None:
                    # Llama a la función que elimina al domain
                    is_deleted = DomainDAO.deleteDomain(id)
                    if is_deleted:
                        return jsonify({'message': 'Domain eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al domain'}), 500
                else:
                    return jsonify({'message': 'Domain no encontrado'}), 404
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401

@domainsMain.before_request
def before_request():
    # Recargar el usuario en cada solicitud
    if current_user.is_authenticated:
        print("Usuario autenticado")