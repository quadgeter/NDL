from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "-------"

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "--"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wlopnykscbmebr:92b1151924463e7ced766b677ba8104d4bf374b0f03625c78c5edcc84627e9e9@ec2-44-199-147-86.compute-1.amazonaws.com:5432/d4suoqn8lh2sq0'
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
