from ..Models import Hosting
from app import db
from .Verifications import Verifications

class HostingDAO():

    @classmethod
    def createHosting(self, data, id):
        try:
            verification_result = Verifications.verificationBuyoutOfCurrentUser(id)
            print("Despues de la verificacion: ")
            print(verification_result)

            if verification_result is not None: 
                newBuyout = verification_result     
            else:
                return {'error': 'No se encontró un usuario loggeado.'}, 401
            
            nuevoHosting = Hosting(**data)

            nuevoHosting.buyout_id = newBuyout

            db.session.add(nuevoHosting)
            db.session.commit()
            return nuevoHosting
        except Exception as ex:
            print("Error:", ex)
            return {'error': 'Ocurrió un error al crear el dominio.'}, 500  # Devolver un código de estado 500
        
    @classmethod
    def getHostings(self):
        try:
            allHostings = Hosting.query.all()
            return allHostings
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getHostingById(self, id):
        try:
            hosting = Hosting.query.filter_by(id=id).first()
            if hosting is not None:
                #hostingJson = hosting.to_JSON()
                return hosting
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updateHosting(self, id, data):
        try:
            hosting = Hosting.query.filter_by(id=id).first()
            if hosting is not None:
                hosting.from_JSON(data)
                db.session.commit()
                hosting_json = hosting.to_JSON()
                return hosting_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deleteHosting(self, id):
        try:
            hosting = Hosting.query.filter_by(id=id).first()
            db.session.delete(hosting)
            db.session.commit()
            return hosting
        except Exception as ex:
            print("error")
            return Exception(ex)

    @classmethod
    def getHostingPlan(self, hosting):
        return hosting.plan