from ..Models import CreditCard
from sqlalchemy.exc import SQLAlchemyError
from app import db

class CreditCardDAO(): 

    @classmethod
    def createCreditCard(self, data):
        try:
            nuevoCreditCard = CreditCard(**data)
            db.session.add(nuevoCreditCard)
            db.session.commit()
            return nuevoCreditCard
        except Exception as ex:
            print("error")
            return Exception(ex)
    
    @classmethod
    def getCreditCards(self):
        try:
            allCreditCards = CreditCard.query.all()
            return allCreditCards
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getCreditCardById(self, id):
        try:
            creditCard = CreditCard.query.filter_by(id=id).first()
            if creditCard is not None:
                return creditCard
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updateCreditCard(self, id, data):
        try:
            creditCard = CreditCard.query.filter_by(id=id).first()
            if creditCard is not None:
                creditCard.from_JSON(data)
                db.session.commit()
                creditCard_json = creditCard.to_JSON()
                return creditCard_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deleteCreditCard(self, id):
        try:
            creditCard = CreditCard.query.filter_by(id=id).first()
            db.session.delete(creditCard)
            db.session.commit()
            return creditCard
        except Exception as ex:
            print("error")
            return Exception(ex)
        