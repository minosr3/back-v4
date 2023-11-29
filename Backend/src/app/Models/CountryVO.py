from app import db

class Country(db.Model):
    __tablename__ = 'Country'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)

    # Relación con la clase User
    #users = db.relationship('User', backref='Country', lazy=True)

    def __init__(self, name):
        self.name = name

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def from_JSON(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])