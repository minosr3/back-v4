from ..Models import PayMode
from sqlalchemy.exc import SQLAlchemyError
from app import db

class PayModeDAO(): 

    @classmethod
    def createPayMode(self, data):
        try:
            nuevoPayMode = PayMode(**data)

            db.session.add(nuevoPayMode)
            db.session.commit()
            return nuevoPayMode
        except Exception as ex:
            print("error")
            return Exception(ex)
    
    @classmethod
    def getPayModes(self):
        try:
            allPayModes = PayMode.query.all()

            payModes = []
            for payMode in allPayModes:
                payModeJson = payMode.to_JSON()
                payModes.append(payModeJson)
            return payModes
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getPayModeById(self, id):
        try:
            payMode = PayMode.query.filter_by(id=id).first()
            if payMode is not None:
                #payModeJson = payMode.to_JSON()
                return payMode
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updatePayMode(self, id, data):
        try:
            payMode = PayMode.query.filter_by(id=id).first()
            if payMode is not None:
                payMode.from_JSON(data)
                db.session.commit()
                payMode_json = payMode.to_JSON()
                return payMode_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deletePayMode(self, id):
        try:
            payMode = PayMode.query.filter_by(id=id).first()
            db.session.delete(payMode)
            db.session.commit()
            return payMode
        except Exception as ex:
            print("error")
            return Exception(ex)