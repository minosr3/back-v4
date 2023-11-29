from app import db

class Plan(db.Model):
    __tablename__ = 'Plan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    control_panel = db.Column(db.String(30))
    cost_per_year = db.Column(db.Integer)
    space = db.Column(db.String(100))
    monthly_traffic = db.Column(db.String(100))
    email_accounts = db.Column(db.Integer)
    databases = db.Column(db.Integer)
    allowed_domains = db.Column(db.Integer)
    supported_cms = db.Column(db.String(100))
    web_server = db.Column(db.String(100))
    security = db.Column(db.String(100))
    site_builder = db.Column(db.String(100))
    backups = db.Column(db.String(100))
    free_ssl = db.Column(db.String(100))

    def __init__(self, name, control_panel, cost_per_year, space, monthly_traffic, email_accounts, databases,
                 allowed_domains, supported_cms, web_server, security, site_builder, backups, free_ssl):
        self.name = name
        self.control_panel = control_panel
        self.cost_per_year = cost_per_year
        self.space = space
        self.monthly_traffic = monthly_traffic
        self.email_accounts = email_accounts
        self.databases = databases
        self.allowed_domains = allowed_domains
        self.supported_cms = supported_cms
        self.web_server = web_server
        self.security = security
        self.site_builder = site_builder
        self.backups = backups
        self.free_ssl = free_ssl

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'control_panel': self.control_panel,
            'cost_per_year': self.cost_per_year,
            'space': self.space,
            'monthly_traffic': self.monthly_traffic,
            'email_accounts': self.email_accounts,
            'databases': self.databases,
            'allowed_domains': self.allowed_domains,
            'supported_cms': self.supported_cms,
            'web_server': self.web_server,
            'security': self.security,
            'site_builder': self.site_builder,
            'backups': self.backups,
            'free_ssl': self.free_ssl
        }

    def from_JSON(self, data):
        for field in ['name', 'control_panel', 'cost_per_year', 'space', 'monthly_traffic', 'email_accounts',
                      'databases', 'allowed_domains', 'supported_cms', 'web_server', 'security', 'site_builder',
                      'backups', 'free_ssl']:
            if field in data:
                setattr(self, field, data[field])

