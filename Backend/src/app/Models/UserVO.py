from sqlalchemy import true
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.Integer)
    idDocument = db.Column(db.String(20))
    document_type = db.Column(db.String(80))
    jobTittle = db.Column(db.String(80), nullable=True)
    direction = db.Column(db.String(120))
    rol_id = db.Column(db.Integer, db.ForeignKey('Rol.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('Country.id'))
    payMode_id = db.Column(db.Integer, db.ForeignKey('PayMode.id'), nullable=True)

    country = db.relationship('Country', backref='user')
    payMode = db.relationship('PayMode', backref='user')
    rol = db.relationship('Rol', backref='user')
    buyouts = db.relationship('Buyout', backref='user', lazy=True)
    creditcards = db.relationship('CreditCard', backref='user', lazy=True)

    def __init__(self, name, email, password, phone, idDocument, document_type,
                 country_id, jobTittle=None, direction=None, payMode_id=None,
                 rol_id=None):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.idDocument = idDocument
        self.document_type = document_type
        self.country_id = country_id
        self.jobTittle = jobTittle
        self.direction = direction
        self.payMode_id = payMode_id
        self.rol_id = rol_id

    def to_JSON(self):

        if self is not None:
            return {
                'id': self.id,
                'name': self.name,
                'email': self.email,
                'phone': self.phone,
                'idDocument': self.idDocument,
                'document_type': self.document_type,
                'country_id': self.country_id,
                'jobTittle': self.jobTittle,
                'direction': self.direction,
                'payMode_id': self.payMode_id,
                'rol_id': self.rol_id,
                'password':self.password
            }
        else: 
            return None

    def from_JSON(self, data):
        for field in ['name', 'email', 'password', 'phone', 'idDocument', 'document_type',
                      'country_id', 'jobTittle', 'direction', 'payMode_id', 'rol_id']:
            if field in data:
                setattr(self, field, data[field])

    @classmethod
    def checkPassword(self, hashedPassword, password):
        return check_password_hash(hashedPassword, password)

    @classmethod
    def convertPassword(self, password):
        return generate_password_hash(password)

    def hashPassword(self):
        passw = self.convertPassword(self.password)
        self.password = passw

    def validateInformationByRol(self):
        if self.rol_id == 1:
            return True
        elif self.rol_id == 2 and not self.jobTittle:
            print('Datos incompletos para empleado(a)')
            return False
        elif self.rol_id == 3:
            print('Información opcional para rol 3')
            return True
        elif not self.rol_id:
            self.rol_id = 1
            return True
        else:
            self.rol_id = 1
            return True
        
            