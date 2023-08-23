from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "playerDB.db"

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "IV"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jqezfrngzgqqxk:8c2fd19ab3fca5815d638d25980bcdceeb7cb0d1c57647bced97cbcfa2c22f30@ec2-3-232-218-211.compute-1.amazonaws.com:5432/d5om337l1m5vv5'
  #  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'        #sqlite database
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Favorite

    with app.app_context():
        db.create_all()


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
