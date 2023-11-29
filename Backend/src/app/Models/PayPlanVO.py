from app import db

class PayPlan(db.Model):
    __tablename__ = 'PayPlan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interval = db.Column(db.String(30), unique=True)

    def __init__(self, interval):
        self.interval = interval

    def to_JSON(self):
        return {
            'id': self.id,
            'interval': self.interval
        }

    def from_JSON(self, data):
        for field in ['interval']:
            if field in data:
                setattr(self, field, data[field])