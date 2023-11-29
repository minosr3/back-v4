from ..Models import Distributor
from app import db

class DistributorDAO():

    @classmethod
    def createDistributor(self, data):
        try:
            nuevoDistributor = Distributor(**data)
            db.session.add(nuevoDistributor)
            db.session.commit()
            return nuevoDistributor
        except Exception as ex:
            print("error")
            return Exception(ex)
    
    @classmethod
    def getDistributors(self):
        try:
            allDistributors = Distributor.query.all()

            distributors = []
            for distributor in allDistributors:
                distributorJson = distributor.to_JSON()
                distributors.append(distributorJson)
            return distributors
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getDistributorById(self, id):
        try:
            distributor = Distributor.query.filter_by(id=id).first()
            if distributor is not None:
                #distributorJson = distributor.to_JSON()
                return distributor
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updateDistributor(self, id, data):
        try:
            distributor = Distributor.query.filter_by(id=id).first()
            if distributor is not None:
                distributor.from_JSON(data)
                db.session.commit()
                distributor_json = distributor.to_JSON()
                return distributor_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deleteDistributor(self, id):
        try:
            distributor = Distributor.query.filter_by(id=id).first()
            db.session.delete(distributor)
            db.session.commit()
            return distributor
        except Exception as ex:
            print("error")
            return Exception(ex)
        
