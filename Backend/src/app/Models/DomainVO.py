from app import db

class Domain(db.Model):
    __tablename__ = 'Domain'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    costDomain = db.Column(db.Integer)
    distributor_id = db.Column(db.Integer, db.ForeignKey('Distributor.id'))
    buyout_id = db.Column(db.Integer, db.ForeignKey('Buyout.id'))  

    # Agregando la relación con Distributor
    distributors = db.relationship('Distributor', backref='domains', lazy=True)

    def __init__(self, name,  distributor_id, buyout_id, costDomain = None):
        self.name = name
        self.costDomain = costDomain
        self.buyout_id = buyout_id
        self.distributor_id = distributor_id

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'costDomain':self.costDomain,
            'distributor_id': self.distributor_id,
            'buyout_id':self.buyout_id
        }

    def from_JSON(self, data):
        for field in ['name', 'costDomain', 'distributor_id', 'buyout_id']:
            if field in data:
                setattr(self, field, data[field])
