from ..Models import Domain
from .Verifications import Verifications
from app import db

class DomainDAO():

    @classmethod
    def createDomain(self, data, id):
        try:
            verification_result = Verifications.verificationBuyoutOfCurrentUser(id)
            print("Despues de la verificacion: ")
            print(verification_result)

            if verification_result is not None: 
                newBuyout = verification_result     
            else:
                return {'error': 'No se encontró un usuario loggeado.'}, 401
            
            print(newBuyout)
            print(data)
            nuevoDomain = Domain(**data)

            nuevoDomain.buyout_id = newBuyout

            print(nuevoDomain.to_JSON()) 

            db.session.add(nuevoDomain)
            db.session.commit()
            return nuevoDomain
        except Exception as ex:
            print("Error:", ex)
            return {'error': 'Ocurrió un error al crear el dominio.'}, 500  # Devolver un código de estado 500
    
    @classmethod
    def getDomains(self):
        try:
            allDomains = Domain.query.all()
            return allDomains
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getDomainById(self, id):
        try:
            domain = Domain.query.filter_by(id=id).first()
            if domain is not None:
                return domain
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updateDomain(self, id, data):
        try:
            domain = Domain.query.filter_by(id=id).first()
            if domain is not None:
                domain.from_JSON(data)
                db.session.commit()
                domain_json = domain.to_JSON()
                return domain_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deleteDomain(self, id):
        try:
            domain = Domain.query.filter_by(id=id).first()
            db.session.delete(domain)
            db.session.commit()
            return domain
        except Exception as ex:
            print("error")
            return Exception(ex)
        
    @classmethod
    def getDomainsDistributors(self, domain):
        return domain.distributors