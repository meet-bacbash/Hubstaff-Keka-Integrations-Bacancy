from app.extensions.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=False, nullable=False)
    keka_id = db.Column(db.String(15), unique=False, nullable=False)
    hubstaff_id = db.Column(db.String(30))
    status = db.Column(db.BIGINT, default = 0)
    hubstaff_name = db.Column(db.String(30))