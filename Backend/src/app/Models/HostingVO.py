from app import db

class Hosting(db.Model):
    __tablename__ = 'Hosting'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hosting_name = db.Column(db.String(50), nullable=False)
    isActive = db.Column(db.Boolean)
    platform_id = db.Column(db.Integer, db.ForeignKey('Platform.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('Plan.id'))
    buyout_id = db.Column(db.Integer, db.ForeignKey('Buyout.id'))  

    # Agregando relaciones con Platform y Plan
    platform = db.relationship('Platform', backref='hostings', lazy=True)
    plan = db.relationship('Plan', backref='hostings', lazy=True)

    def __init__(self, hosting_name, isActive, platform_id, plan_id, buyout_id):
        self.hosting_name = hosting_name
        self.isActive = self.isActive
        self.platform_id = platform_id
        self.plan_id = plan_id
        self.buyout_id = buyout_id

    def to_JSON(self):
        return {
            'id': self.id,
            'hosting_name': self.hosting_name,
            'isActive': self.isActive,
            'platform_id': self.platform_id,
            'plan_id': self.plan_id,
            'buyout_id':self.buyout_id
        }

    def from_JSON(self, data):
        for field in ['hosting_name', 'isActive', 'platform_id', 'plan_id', 'buyout_id']:
            if field in data:
                setattr(self, field, data[field])