from ..Models import User
from app import db

class LoginService():
# Clase que se encarga de la verificacion mediante el email
    @classmethod
    def login(self, email, password):
        try:
            user = User.query.filter_by(email=email).first()
            if user is not None:
                isPasswordCorrect = User.checkPassword(user.password, password)
                user.password = isPasswordCorrect
                return user
            else:
                return None
        except Exception as ex:
            print("error 007")
            raise Exception(ex)