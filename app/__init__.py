from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(conf_name):
    app = Flask(__name__)
    conf = config[conf_name]
    app.config.from_object(conf)
    conf.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        from datetime import date
        from app.models import Temperature, Place


    login_manager.init_app(app)
    from app.main import main as main_bl
    from app.auth import auth as auth_bl
    from app.api import api as api_bl
    app.register_blueprint(main_bl)
    app.register_blueprint(auth_bl)
    app.register_blueprint(api_bl, url_prefix='/api')

    return app
