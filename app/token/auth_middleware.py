"""
Authorization middleware for authenticate if user is already logged in or authorized user or not.
"""

from functools import wraps
import jwt
from flask import request, redirect, session, flash,g
from app.model import Credentials
from app.extensions.db import app


def token_required(f):
    """
    it will check for the token
    If token not fond -> redirect to login page

    :param f:
    :return:
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('Authorization')
        if not token:
            return redirect('/login')
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except Exception as ex:
            print(ex)

        return f(*args, **kwargs)
    return decorated


def token_already_exist(f):
    """
    It will be used when already one session is going on and user tries to login again
    if the session is ongoing -> restrict user from login/register
    :param f:
    :return:
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('Authorization')
        if not token:
            return f(*args, **kwargs)
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            if data:
                return redirect('/')
        except Exception as ex:
            print(ex)
            return f(*args, **kwargs)

        return f(*args, **kwargs)

    return decorated
