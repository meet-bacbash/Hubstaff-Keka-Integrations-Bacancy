"""
It contains all the models used in app
"""
from app.extensions.db import db

class User(db.Model):
    """
    User model contains details of employees
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    keka_id = db.Column(db.String(15), unique=True, nullable=False)
    hubstaff_id = db.Column(db.String(30))
    status = db.Column(db.BIGINT, default = 0)
    hubstaff_name = db.Column(db.String(30))

class Credentials(db.Model):
    """
    Credentials model contains all the admin creds
    """
    __tablename__ = "credentials"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
