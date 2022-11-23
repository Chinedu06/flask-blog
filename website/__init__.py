from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_user

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    app.app_context().push()
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    from . import models
    from .models import User, Post, Comment, Like
    
    with app.app_context():
        db.create_all()
    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    

        
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
        
    return app   


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all()
        # print('Created database')