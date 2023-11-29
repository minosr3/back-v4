from ..Models import Rol
from sqlalchemy.exc import SQLAlchemyError
from app import db

class RolDAO(): 

    @classmethod
    def createRol(self, data):
        try:
            nuevoRol = Rol(**data)
            db.session.add(nuevoRol)
            db.session.commit()
            return Rol
        except Exception or SQLAlchemyError as ex:
            print("error")
            return Exception(ex)
    
    @classmethod
    def getRols(self):
        try:
            allRols = Rol.query.all()

            rols = []
            for rol in allRols:
                rolJson = rol.to_JSON()
                rols.append(rolJson)
            return rols
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getRolById(self, id):
        try:
            rol = Rol.query.filter_by(id=id).first()
            if rol is not None:
                return rol
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updateRol(self, id, data):
        try:
            rol = Rol.query.filter_by(id=id).first()
            if rol is not None:
                rol.from_JSON(data)
                db.session.commit()
                rol_json = rol.to_JSON()
                return rol_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deleteRol(self, id):
        try:
            rol = Rol.query.filter_by(id=id).first()
            db.session.delete(rol)
            db.session.commit()
            return rol
        except Exception as ex:
            print("error")
            return Exception(ex)