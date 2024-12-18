from flask import session, redirect, render_template, make_response, flash, request, url_for
from app.model import User
from app.extensions.db import app
from app.extensions.db import db

@app.route('/login', methods=['GET', 'POST'])
def log_in():
    ''' Login page'''
    users = User.query.all()
    return render_template('auth-login-basic.html',users = users)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    ''' Login page'''
    return render_template('auth-register-basic.html')

@app.route('/', methods=['GET', 'POST'])
def home_page():
    ''' Login page'''
    total_user = User.query.count()
    active_users = User.query.where(User.status==1).count()
    return render_template('index.html',total_user=total_user, active_users=active_users)

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    ''' Login page'''
    return render_template('profile-page.html')

@app.route('/user_details', methods=['GET', 'POST'])
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
    return render_template('user-details.html', users = users)

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
            return redirect('user_details')
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
            return redirect('user_details')
    return redirect('user_details')
