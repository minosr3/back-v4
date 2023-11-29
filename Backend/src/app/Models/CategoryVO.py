from app import db

class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100))
    commission = db.Column(db.Integer)

    def __init__(self, category_name, commission):
        self.category_name = category_name
        self.commission = commission

    def to_JSON(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'commission': self.commission
        }

    def from_JSON(self, data):
        for field in ['category_name', 'commission']:
            if field in data:
                setattr(self, field, data[field])