from ..Models import Country
from sqlalchemy.exc import SQLAlchemyError
from app import db

class CountryDAO(): 

    @classmethod
    def createCountry(self, data):
        try:
            nuevoCountry = Country(**data)
            db.session.add(nuevoCountry)
            db.session.commit()
            return nuevoCountry
        except Exception as ex:
            print("error")
            return Exception(ex)
    
    @classmethod
    def getCountrys(self):
        try:
            allCountrys = Country.query.all()

            countrys = []
            for country in allCountrys:
                countryJson = country.to_JSON()
                countrys.append(countryJson)
            return countrys
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getCountryById(self, id):
        try:
            country = Country.query.filter_by(id=id).first()
            if country is not None:
                return country
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updateCountry(self, id, data):
        try:
            country = Country.query.filter_by(id=id).first()
            if country is not None:
                country.from_JSON(data)
                db.session.commit()
                country_json = country.to_JSON()
                return country_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deleteCountry(self, id):
        try:
            country = Country.query.filter_by(id=id).first()
            db.session.delete(country)
            db.session.commit()
            return country
        except Exception as ex:
            print("error")
            return Exception(ex)