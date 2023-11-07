
from flask import Blueprint, render_template, request, flash, redirect, url_for 
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 
        remember = request.form.get('rememberMe')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Welcome! Login Successful.', category='success')
                login_user(user, remember=remember)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid Username or Password, Please Try Again.', category='error')
        else:
                flash('Invalid Username or Password, Please Try Again.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        agree = request.form.get('agree')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username is already taken.', category='error')
            return redirect(url_for('auth.sign_up'))
        if len(username) < 2:
            flash('Username must be at least 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 5:
            flash('Password must be 6 or more characters', category='error')
        #elif agree != 'on':
        #    flash('You must agree to the terms.', category='error')
        else: 
            new_user = User(username=username, password=generate_password_hash(password1, method='scrypt'), language="en", defaultsort="Task.date")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account successfully created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', category='error')
            return redirect("/settings")
        elif new_password != confirm_password:
            flash('New password and confirm password do not match.', category='error')
            return redirect("/settings")
        elif len(new_password) < 6:
            flash('New password must be 6 or more characters.', category='error')
            return redirect("/settings")
        else:
            flash('Password successfully changed.', category='error')
            current_user.password = generate_password_hash(new_password, method='scrypt')
            db.session.commit()
            return redirect("/settings")

    return render_template("Settings.html", user=current_user)




@auth.route('/change-username', methods=['GET', 'POST'])
@login_required
def change_username():
    if request.method == 'POST':
        username = request.form.get('username')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username is already taken.', category='error')
        elif len(username) < 2:
            flash('Username must be at least 3 characters.', category='error')
        else:
            flash('Username successfully changed.', category='error')
            current_user.username = username
            db.session.commit()
            
        return redirect("/settings")
    return render_template("Settings.html", user=current_user)
    