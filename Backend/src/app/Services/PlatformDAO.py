from ..Models import Platform
from sqlalchemy.exc import SQLAlchemyError
from app import db

class PlatformDAO(): 

    @classmethod
    def createPlatform(self, data):
        try:
            nuevoPlatform = Platform(**data)

            db.session.add(nuevoPlatform)
            db.session.commit()
            return nuevoPlatform
        except Exception as ex:
            print("error")
            return Exception(ex)
    
    @classmethod
    def getPlatforms(self):
        try:
            allPlatforms = Platform.query.all()

            platforms = []
            for platform in allPlatforms:
                platformJson = platform.to_JSON()
                platforms.append(platformJson)
            return platforms
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getPlatformById(self, id):
        try:
            platform = Platform.query.filter_by(id=id).first()
            if platform is not None:
                #platformJson = platform.to_JSON()
                return platform
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updatePlatform(self, id, data):
        try:
            platform = Platform.query.filter_by(id=id).first()
            if platform is not None:
                platform.from_JSON(data)
                db.session.commit()
                platform_json = platform.to_JSON()
                return platform_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deletePlatform(self, id):
        try:
            platform = Platform.query.filter_by(id=id).first()
            db.session.delete(platform)
            db.session.commit()
            return platform
        except Exception as ex:
            print("error")
            return Exception(ex)