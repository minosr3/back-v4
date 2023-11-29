from app import db

class Platform(db.Model):
    __tablename__ = 'Platform'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def from_JSON(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])