from ..Models import Category
from app import db

class CategoryDAO():

    @classmethod
    def createCategory(self, data):
        try:
            nuevoCategory = Category(**data)
            db.session.add(nuevoCategory)
            db.session.commit()
            return nuevoCategory
        except Exception as ex:
            print("error")
            return Exception(ex)
    
    @classmethod
    def getCategorys(self):
        try:
            allCategorys = Category.query.all()

            categorys = []
            for category in allCategorys:
                categoryJson = category.to_JSON()
                categorys.append(categoryJson)
            return categorys
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getCategoryById(self, id):
        try:
            category = Category.query.filter_by(id=id).first()
            if category is not None:
                return category
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updateCategory(self, id, data):
        try:
            category = Category.query.filter_by(id=id).first()
            if category is not None:
                category.from_JSON(data)
                db.session.commit()
                category_json = category.to_JSON()
                return category_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deleteCategory(self, id):
        try:
            category = Category.query.filter_by(id=id).first()
            db.session.delete(category)
            db.session.commit()
            return category
        except Exception as ex:
            print("error")
            return Exception(ex)