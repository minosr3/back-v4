from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from .utils import finalConfig
from flask_cors import CORS
from .utils import loginManagerApp#, csrf

db = SQLAlchemy()

def createApp(config_name):
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.from_object(finalConfig[config_name])

    db.init_app(app)
    

    loginManagerApp.init_app(app)

    '''#csrf.init_app(app)'''
    

    # rutas
    from app import Routes
    

    # Error handlers
    app.register_error_handler(401, Routes.authRoutes.status401)
    app.register_error_handler(404, Routes.authRoutes.status404)

    return app
