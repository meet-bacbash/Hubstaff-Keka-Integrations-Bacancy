"""
All the APP, DATABASE, SESSION, BCRYPT related initialization are done here
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

SECRET_KEY = os.urandom(32)

BASE_DIR = '/home/bacancy/Programming/python/hubstaff_website'

app = Flask(
    __name__,
    template_folder= os.path.join(BASE_DIR,"templates"),
    static_folder=os.path.join(BASE_DIR,"static"),
    static_url_path="/",
)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
# print('=============================================================')
# print(app.config['SQLALCHEMY_DATABASE_URI'])
# print('=============================================================')

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

def create_db():
    """ it will create model table if not exist."""
    from app.model import User

    with app.app_context():
        db.create_all()
