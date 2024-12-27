"""
All the routes used in app are inside routes folder
"""
import os
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

import jwt
from flask import redirect, render_template, request, g
from flask import session, make_response, flash, send_from_directory

from app.model import User, Credentials
from app.extensions.db import app
from app.extensions.db import db, bcrypt
from app.token.auth_middleware import token_required,token_already_exist
from app.hubstaff import hubstaff_id_sync


DOWNLOADS_FOLDER = "/home/bacancy/Programming/python/hubstaff_website/Downloads"

# AUTH ROUTES

@app.route('/login', methods=['GET', 'POST'])
@token_already_exist
def log_in():
    """
    Handles user login.

    Methods:
        GET: Renders the login page.
        POST: Processes login form data, validates user credentials, and generates a JWT token
              for the session if valid.

    Behavior:
        - Checks if the user exists in the database.
        - Verifies the password using bcrypt.
        - Generates a JWT token with a 30-minute expiration time upon successful login.
        - Stores the token in cookies and username in the session.
        - Redirects to the home page if successful, otherwise displays an error message.

    Returns:
        Response: Redirects to the home page on success or renders the login page with an error.
    """
    if request.method == 'POST':
        if 'login' in request.form:
            data = request.form.to_dict()
            username = data['username']
            password = data['password']
            user = Credentials.query.filter(Credentials.username == username).first()
            original_password = user.password
            is_valid = bcrypt.check_password_hash(original_password, password)
            if is_valid:
                token = jwt.encode(
                    {"username": username,
                     'exp': datetime.now() + timedelta(hours=5)},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                response = make_response(redirect('/'))
                response.set_cookie("Authorization", token)
                session['username'] = username
                return response
            else:
                flash("Please enter valid username and password")
    return render_template('/auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
@token_already_exist
def register_user():
    """
    Handles user registration by adding a new user to the database.

    Methods:
        GET: Renders the registration page.
        POST: Processes the registration form, creates a new user, and saves to the database.

    Returns:
        Response: Redirects to the login page or renders the registration page.
    """
    if request.method == 'POST':
        if 'register' in request.form:
            data = request.form.to_dict()
            username = data['username']
            password = data['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_admin = Credentials(username = username, password = hashed_password)
            try:
                db.session.add(new_admin)
                db.session.commit()
                flash("User registered found")
                redirect('login')
            except Exception as e:
                db.session.rollback()  # Rollback if there's an error
                flash("An error occurred while registering the user ! Please try again")
    return render_template('/auth/register.html')


@app.route('/logout')
def logout():
    """
    Logs out the user by clearing the session and deleting the authorization cookie.

    Returns:
        response (Response): Redirects to the login page after clearing the session.
    """
    session.clear()
    response = make_response(redirect('/login'))
    response.delete_cookie("Authorization")
    return response


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    """
    Renders the forgot password page.

    Returns:
        Response: Renders the forgot password template.
    """
    return render_template('/auth/forgot-password.html')

# USER DETAILS ROUTES

@app.route('/', methods=['GET', 'POST'])
@token_required
def user_details():
    """
    Displays the user details page and handles edit/delete operations.

    Methods:
        GET: Retrieves all users and renders the user details page.
        POST: Handles delete operations based on the form submission.

    Returns:
        Response: Renders the user details page.
    """
    username = session.get('username')
    if request.method == 'POST':
        if 'delete-button' in request.form:
            data = request.form.to_dict()
            print(data['keka_id'])
            user = User.query.filter(User.keka_id == data['keka_id']).first()
            if user:
                try:
                    db.session.delete(user)  # Mark the user for deletion
                    db.session.commit()  # Commit the transaction
                    flash("User deleted successfully")
                except Exception as e:
                    db.session.rollback()  # Rollback if there's an error
                    flash("Error occurred while deleting user! Please try again later")
            else:
                flash("User not found")
    users = User.query.all()
    return render_template('user-details.html', users = users, page_name = "home", username = username)

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    """
    Handles the addition of new users.

    Methods:
        GET: Renders the add user page.
        POST: Processes the add user form and saves the user to the database.

    Returns:
        Response: Redirects to the home page or renders the add user page.
    """
    if request.method == 'POST':
        if 'add-details' in request.form:
            data = request.form.to_dict()
            name = data['name']
            email = data['email']
            keka_id = data['keka_id']
            print(name, email, keka_id)
            hubstaff_id = hubstaff_id_sync(email=email)
            if hubstaff_id:
                new_user = User(keka_id=keka_id, name=name, email=email, status = 1, hubstaff_id = hubstaff_id)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash("User added successfully")
                    return redirect('/')
                except IntegrityError as e:
                    flash("User already exist")
                    return redirect('/')
                except Exception as e:
                    db.session.rollback()  # Rollback if there's an error
                    flash("Error occurred while adding new user! Please try again later")
            else:
                new_user = User(keka_id=keka_id, name=name, email=email)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash("User added successfully")
                    flash(f"Hubstaff account not found for {email}")
                    return redirect('/')
                except IntegrityError as e:
                    flash("User already exist")
                    return redirect('/')
                except Exception as e:
                    db.session.rollback()  # Rollback if there's an error
                    flash("Error occurred while adding new user! Please try again later")
    return render_template('add-user.html')


@app.route('/edit_user', methods=['POST'])
def edit_user():
    """
    Handles editing and updating user details.

    Methods:
        POST: Processes the edit user form, updates the user details, and saves to the database.

    Returns:
        Response: Redirects to the home page or renders the edit user page.
    """
    if request.method == 'POST':
        if 'edit-button' in request.form:
            data = request.form.to_dict()
            user_detail = User.query.filter(User.keka_id == data['keka_id']).first()
            if user_detail:
                return render_template('edit-user.html',user_detail = user_detail)
            else:
                flash("User details not found")

        if 'update-details' in request.form:
            data = request.form.to_dict()
            print(data['keka_id'])
            user = User.query.filter(User.keka_id == data['keka_id']).first()
            user.name = data['name']
            user.email = data['email']
            if user:
                try:
                    db.session.commit()
                    flash("User details updated successfully")
                except Exception as e:
                    db.session.rollback()  # Rollback if there's an error
                    flash(f"Error occurred while updating user details ")
            else:
                flash("Error in updating the details")
            return redirect('/')
    return redirect('/')


# TIMESHEET ROUTES

@app.route('/timesheets', methods=['GET'])
@token_required
def view_timesheets():
    """
    Displays the timesheet page by listing all available timesheet files.

    Returns:
        Response: Renders the timesheet page with a list of timesheets.
    """
    dir_list = [os.path.splitext(file)[0] for file in os.listdir(DOWNLOADS_FOLDER) if os.path.isfile(os.path.join(DOWNLOADS_FOLDER, file))]
    return render_template('timesheet-page.html', timesheets = dir_list, page_name = "timesheet")

@app.route('/download/<filename>')
def download_file(filename):
    """
    Allows downloading of a specified file from the downloads folder.

    Args:
        filename (str): The name of the file to be downloaded.

    Returns:
        Response: Sends the file as an attachment for download.
    """
    # Serve the file for download
    return send_from_directory(DOWNLOADS_FOLDER, filename, as_attachment=True)


# ERROR ROUTES

@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    """
    Handles 404 errors and displays the custom 404 error page.

    Args:
        e (Exception): The exception object for the 404 error.

    Returns:
        Response: Renders the 404 error page template.
    """
    # defining function
    return render_template("404_page.html")
