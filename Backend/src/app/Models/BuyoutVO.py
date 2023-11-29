from app import db

class Buyout(db.Model):
    __tablename__ = 'Buyout'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    pay_plan_id = db.Column(db.Integer, db.ForeignKey('PayPlan.id'), nullable=False)

    # Agregando relaciones con User, Hosting, Domain, y PayPlan
    hostings = db.relationship('Hosting', backref='buyout', lazy=True)
    domains = db.relationship('Domain', backref='buyout', lazy=True)
    pay_plan = db.relationship('PayPlan', backref='buyouts', lazy=True)

    def __init__(self, user_id, pay_plan_id, status='Pending'):
        self.user_id = user_id
        self.pay_plan_id = pay_plan_id
        self.status = status

    def to_JSON(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pay_plan_id': self.pay_plan_id,
            'status':self.status
        }

    def from_JSON(self, data):
        for field in ['user_id', 'pay_plan_id', 'status']:
            if field in data:
                setattr(self, field, data[field])
