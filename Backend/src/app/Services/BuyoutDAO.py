from ..Models import Buyout
from sqlalchemy.exc import SQLAlchemyError
from app import db

class BuyoutDAO(): 

    @classmethod
    def createBuyout(self, data):
        try:
            user_id = data.get('user_id')
            existing_buyout = Buyout.query.filter_by(user_id=user_id).filter(Buyout.status == 'Pending').first()
            if not existing_buyout:
                nuevoBuyout = Buyout(**data)
                db.session.add(nuevoBuyout)
                db.session.commit()
                return nuevoBuyout
            else: 
                 return {'error': 'El usuario ya tiene un Buyout en estado Pending.'}
        except Exception as ex:
            print("error")
            return Exception(ex)
    
    @classmethod
    def getBuyouts(self):
        try:
            allBuyouts = Buyout.query.all()
            return allBuyouts
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getBuyoutById(self, id):
        try:
            buyout = Buyout.query.filter_by(id=id).first()
            if buyout is not None:
                return buyout
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updateBuyout(self, id, data):
        try:
            buyout = Buyout.query.filter_by(id=id).first()
            if buyout is not None:
                buyout.from_JSON(data)
                db.session.commit()
                buyout_json = buyout.to_JSON()
                return buyout_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deleteBuyout(self, id):
        try:
            buyout = Buyout.query.filter_by(id=id).first()
            db.session.delete(buyout)
            db.session.commit()
            return buyout
        except Exception as ex:
            print("error")
            return Exception(ex)
        
    @classmethod
    def getBuyoutsDomains(self, buyout):
        return buyout.domains
        #return [domain.to_JSON() for domain in buyout.domains]

    @classmethod
    def getBuyoutsHostings(self, buyout):
        return buyout.hostings
        #return [hosting.to_JSON() for hosting in buyout.hostings]