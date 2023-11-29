from flask_login import current_user
from ..Models import Buyout, Domain, Hosting, CreditCard
from .BuyoutDAO import BuyoutDAO
from app import db

class Verifications():

    """
    Verifica si el usuario tiene un buyout en estado 'Pending'. Crea uno si no existe.
    :param id_user: ID del usuario.
    :return: ID del buyout.
    """
    @classmethod
    def verificationBuyoutOfCurrentUser(self, idUser):
        # Obtener el ID del usuario loggeado
        try: 
            user_id = current_user.id if current_user.is_authenticated else idUser
            # Verificar si el usuario tiene un Buyout en estado 'Pending'

            if user_id is not None:
                existing_pending_buyout = Buyout.query.filter_by(user_id=user_id, status='Pending').first()
                if not existing_pending_buyout:
                    print('el usuario no tiene buyout')
                    data = self.createPendingBuyout(user_id)
                    print(data.to_JSON())
                    db.session.add(data)
                    db.session.commit()
                    # Refrescar la instancia después del commit para obtener el ID autoincrementable
                    db.session.refresh(data)

                    print('Buyout creado y guardado en la base de datos con ID:', data.id)
                    return data.id
                else: 
                    print('Si hay un buyout')
                    return existing_pending_buyout.id  
            else: 
                print("No hay usuario loggeado")
                return None
        except Exception as ex:
            print("error verification 001")
            return Exception(ex)
        
    """
    Crea datos para un buyout pendiente.
    :param user_id: ID del usuario.
    :return: Datos del buyout pendiente.
    """
    @classmethod
    def createPendingBuyout(cls, user_id):
        return Buyout(pay_plan_id=1, status="Pending", user_id=user_id)
    
    """
    Obtiene elementos del usuario por tipo (Buyout, CreditCard).
    :param id_user: ID del usuario.
    :param item_type: Tipo de elemento ('Buyout' o 'CreditCard').
    :return: Lista de elementos.
    """
    @classmethod
    def get_itemsOfCurrentUser(cls, idUser, item_type):
        user_id = current_user.id if current_user.is_authenticated else idUser
        if user_id is not None:
            if item_type == 'Buyout':
                return Buyout.query.filter_by(user_id=user_id).all()
            elif item_type == 'CreditCard':
                return CreditCard.query.filter_by(user_id=user_id).all()
        return None
        
    """
    Obtiene elementos de un modelo de usuario específico relacionados con un usuario dado.

    :param user_model: El modelo de usuario del cual obtener elementos (por ejemplo, Domain, Hosting, etc.).
    :param user_id: El ID del usuario. Si no se proporciona, se intentará obtener el ID del usuario autenticado.
    :return: Una lista de elementos del modelo de usuario relacionados con el usuario identificado por user_id.
             Retorna None si no se proporciona un user_id o si no hay usuario autenticado.
    """
    @classmethod
    def getItemsOfUser(cls, user_model, user_id=None):
        user_id = current_user.id if current_user.is_authenticated else user_id
        if user_id is not None:
            return user_model.query.join(Buyout).filter(Buyout.user_id == user_id).all()
        else:
            return None

    @classmethod
    def getDomainsOfCurrentUser(cls, user_id=None):
        return cls.getItemsOfUser(Domain, user_id)

    @classmethod
    def getHostingsOfCurrentUser(cls, user_id=None):
        return cls.getItemsOfUser(Hosting, user_id)
    

# Ejemplo de uso
#user_buyouts = UserItemFactory.get_items(current_user.id, 'Buyout')
#user_credit_cards = UserItemFactory.get_items(current_user.id, 'CreditCard')
