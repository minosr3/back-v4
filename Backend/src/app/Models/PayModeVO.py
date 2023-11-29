from app import db

class PayMode(db.Model):
    __tablename__ = 'PayMode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)

    # Relación con la clase User
    #users = db.relationship('User', backref='PayMode', lazy=True)

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
