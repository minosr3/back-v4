from ..Models import User
from .CountryDAO import CountryDAO
from .RolDAO import RolDAO
from .PayModeDAO import PayModeDAO
from app import db


class UserDAO():

    # Obtener la lista de usuarios
    @classmethod
    def getUsers(self):
        try:
            users = User.query.all()
            return users
        except Exception as ex:
            print(f"Error: {ex}")
            raise Exception(ex)

    # Obtener la un usuario por un id 
    @classmethod
    def getUserByID(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            return user
        except Exception as ex:
            print(f"Error: {ex}")
            raise Exception(ex)

    @classmethod
    def getUserByEmail(self, email):
        try:
            user = User.query.filter_by(email=email).first()
            return user
        except Exception as ex:
            print(f"Error: {ex}")
            raise Exception(ex)

    # Crear User sin el hash
    @classmethod
    def create_User(self, data):
        try:
            nuevoUser = User(**data)

            db.session.add(nuevoUser)
            db.session.commit()
            return nuevoUser
        except Exception as ex:
            print(f"Error: {ex}")
            return Exception(ex)

    # Clase que actualiza el usuario
    @classmethod
    def uptadeUser(self, id, data):
        try:
            user = User.query.filter_by(id=id).first()
            if user is not None:
                user.from_JSON(data)
                if 'password' in data:
                    user.hashPassword()
                db.session.commit()
                user_json = user.to_JSON()
                return user_json
            else:
                return False
        except Exception as ex:
            print(f"Error: {ex}")
            raise Exception(ex)

    # Clase que elimina el usuario
    @classmethod
    def deleteUser(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            db.session.delete(user)
            db.session.commit()
            return user
        except Exception as ex:
            print(f"Error: {ex}")
            return Exception(ex)

    # Crearte user con el hash
    @classmethod
    def createUser(self, data):
        try:
            nuevoUser = User(**data)
            
            if(nuevoUser.validateInformationByRol()):
                nuevoUser.hashPassword()
                db.session.add(nuevoUser)
                db.session.commit()
                return nuevoUser
            else: 
                print("error 013")
                return None
        except Exception as ex:
            print(f"Error: {ex}")
            return Exception(ex)

    @classmethod
    def getDetailsToUser(cls, user): 
        try: 
            if user is None:
                return None, None, None  # O retorna algún valor predeterminado que tenga sentido en tu contexto
            country = CountryDAO.getCountryById(user.country_id)
            countryJson = country.to_JSON() if country else None

            rol = RolDAO.getRolById(user.rol_id)
            rolJson = rol.to_JSON() if rol else None

            payMode = PayModeDAO.getPayModeById(user.payMode_id)
            payModeJson = payMode.to_JSON() if payMode else None

            return countryJson, rolJson, payModeJson
        except Exception as ex: 
            print(f"Error: {ex}")
            return (f"Error 014: {ex}")
        
    @classmethod
    def getUserBuyout(self, user):
        return user.buyouts

