import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
# init SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:132003@localhost/flaskdb'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)


class User(UserMixin, db.Model):

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)


with app.app_context():
    db.create_all()

    # blueprint for auth routes in our app
from .auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app

from .main import main as main_blueprint

app.register_blueprint(main_blueprint)
