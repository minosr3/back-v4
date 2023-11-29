from app import db

class CreditCard(db.Model):
    __tablename__ = 'CreditCard'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    card_number = db.Column(db.String(16), nullable=False)
    expiration_date = db.Column(db.String(5), nullable=False)
    cardholder_name = db.Column(db.String(100), nullable=False)
    cvscard = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __init__(self, card_number, expiration_date, cardholder_name, user_id, cvscard):
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cardholder_name = cardholder_name
        self.user_id = user_id
        self.cvscard = cvscard

    def to_JSON(self):
        return {
            'id': self.id,
            'card_number': self.card_number,
            'expiration_date': self.expiration_date,
            'cardholder_name': self.cardholder_name,
            'user_id': self.user_id,
            'cvscard': self.cvscard
        }

    def from_JSON(self, data):
        for field in ['card_number', 'expiration_date', 'cardholder_name', 'user_id', 'cvscard']:
            if field in data:
                setattr(self, field, data[field])