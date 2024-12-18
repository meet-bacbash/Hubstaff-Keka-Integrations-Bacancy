'''
Main Database connection is done here
'''
import os
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
# from flask_msearch import Search
# from flask_mail import Mail

SECRET_KEY = os.urandom(32)

BASE_DIR = '/home/bacancy/Programming/python/hubstaff_website'

print("===============================")
app = Flask(
    __name__,
    template_folder= os.path.join(BASE_DIR,"templates"),
    static_folder=os.path.join(BASE_DIR,"static"),
    static_url_path="/",
)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
print('=============================================================')
print(app.config['SQLALCHEMY_DATABASE_URI'])
print('=============================================================')

app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)


def create_db():
    ''' it will create model table if not exist.'''
    from app.model import User

    with app.app_context():
        db.create_all()

