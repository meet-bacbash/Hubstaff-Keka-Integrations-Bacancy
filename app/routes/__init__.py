import os

from flask import session, redirect, render_template, make_response, flash, request, url_for, send_from_directory

from app.model import User, Credentials
from app.extensions.db import app
from app.extensions.db import db, bcrypt

DOWNLOADS_FOLDER = "/home/bacancy/Programming/python/hubstaff_website/Downloads"

@app.route('/login', methods=['GET', 'POST'])
def log_in():
    ''' Login page'''
    if request.method == 'POST':
        if 'login' in request.form:
            data = request.form.to_dict()
            username = data['username']
            password = data['password']
            user = Credentials.query.filter(Credentials.username == username).first()
            original_password = user.password
            is_valid = bcrypt.check_password_hash(original_password, password)
            if is_valid:
                return redirect('/')
            else:
                flash("Please enter valid username and password")
    return render_template('/auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    ''' Login page'''
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
            except Exception as e:
                db.session.rollback()  # Rollback if there's an error
                flash(f"An error occurred while registering the user")
            redirect('login')
    return render_template('/auth/register.html')

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    ''' Login page'''
    return render_template('/auth/forgot-password.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    ''' Login page'''
    return render_template('profile-page.html')

@app.route('/', methods=['GET', 'POST'])
def user_details():
    ''' Login page'''
    if request.method == 'POST':
        if 'edit-button' in request.form:
            data = request.form.to_dict()
            print(data['keka_id'])
            redirect(edit_user)
        elif 'delete-button' in request.form:
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
                    flash(f"An error occurred: {e}")
            else:
                flash("User not found")
    users = User.query.all()
    return render_template('user-details.html', users = users, page_name = "home")

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    '''
    add user page
    '''
    if request.method == 'POST':
        if 'add-details' in request.form:
            data = request.form.to_dict()
            name = data['name']
            email = data['email']
            keka_id = data['keka_id']
            print(name, email, keka_id)
            new_user = User(keka_id=keka_id, name=name, email=email)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("User added successfully")
            except Exception as e:
                db.session.rollback()  # Rollback if there's an error
                flash(f"An error occurred: {e}")
            return redirect('/')
    return render_template('add-user.html')


@app.route('/edit_user', methods=['POST'])
def edit_user():
    ''' Login page'''
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
                    flash(f"An error occurred: {e}")
            else:
                flash("Error in updating the details")
            return redirect('/')
    return redirect('/')

@app.route('/timesheets', methods=['GET'])
def view_timesheets():
    dir_list = [os.path.splitext(file)[0] for file in os.listdir(DOWNLOADS_FOLDER) if os.path.isfile(os.path.join(DOWNLOADS_FOLDER, file))]
    return render_template('timesheet-page.html', timesheets = dir_list, page_name = "timesheet")

@app.route('/download/<filename>')
def download_file(filename):
    # Serve the file for download
    return send_from_directory(DOWNLOADS_FOLDER, filename, as_attachment=True)



@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("404_page.html")