from app import db

class Distributor(db.Model):
    __tablename__ = 'Distributor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    number_domains = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'))

    # Agregando la relación con Category
    category = db.relationship('Category', backref='distributors', lazy=True)

    def __init__(self, name, number_domains, category_id = None):
        self.name = name
        self.number_domains = number_domains
        self.category_id = category_id
        self.setCategory()

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'number_domains': self.number_domains,
            'category_id': self.category_id
        }

    def from_JSON(self, data):
        for field in ['name', 'number_domains', 'category_id']:
            if field in data:
                setattr(self, field, data[field])

    def setCategory(self):
        if self.category_id is None:
            self.category_id = 1 if 0 <= self.number_domains <= 100 else 2
        elif self.category_id not in [1, 2]:
            raise ValueError("El category_id especificado no es válido.")
        elif (self.category_id == 1 and self.number_domains > 100) or (self.category_id == 2 and self.number_domains <= 100):
            self.category_id = 3 - self.category_id
        else:
            raise ValueError("La combinación de category_id y número de dominios no es válida.")

    