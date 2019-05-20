import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_mail import Mail
from datetime import timedelta
from flask_login import LoginManager 
from magic.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'warning'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from magic.main.routes import main
    from magic.errors.handlers import errors
    from magic.admin.routes import admin
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(admin)
    

    return app 




