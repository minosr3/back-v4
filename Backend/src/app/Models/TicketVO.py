from app import db

class Ticket(db.Model):
    __tablename__ = 'Ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text)
    state = db.Column(db.Boolean, nullable=False)
    priority = db.Column(db.Integer)
    services = db.Column(db.Text)  # Nueva columna para servicios
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user_it_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    # Agregando relaciones con User
    user = db.relationship('User', foreign_keys=[user_id], backref='created_tickets', lazy=True)
    user_it = db.relationship('User', foreign_keys=[user_it_id], backref='assigned_tickets', lazy=True)

    def __init__(self, description, message, services, state, priority, user_id, user_it_id=None):
        self.description = description
        self.message = message
        self.services = services  # Ajustado para incluir la columna 'services'
        self.state = state
        self.priority = priority
        self.user_id = user_id
        self.user_it_id = user_it_id

    def to_JSON(self):
        return {
            'id': self.id,
            'description': self.description,
            'message': self.message,
            'services': self.services,  # Ajustado para incluir 'services'
            'state': self.state,
            'priority': self.priority,
            'user_id': self.user_id,
            'user_it_id': self.user_it_id
        }

    def from_JSON(self, data):
        for field in ['description', 'message', 'services', 'state', 'priority', 'user_id', 'user_it_id']:
            if field in data:
                setattr(self, field, data[field])
