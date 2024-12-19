"""
App init file which have create_app function which will be used to initialize the app in the server
"""

from app.extensions.db import app, create_db
from flask_session import Session

def create_app():
    """
    Handles the initialization of the app from the main file
    :return: app object
    """
    Session(app)
    create_db()

    upload_folder = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = upload_folder

    # file import
    from app.model import User
    from app.extensions import db
    from app import routes

    return app
