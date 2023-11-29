from app import db

class Rol(db.Model):
    __tablename__ = 'Rol'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.Text, nullable=True)

    # Relación con la clase User
    #users = db.relationship('User', backref='Rol', lazy=True)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

    def from_JSON(self, data):
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])
