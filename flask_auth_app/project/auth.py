from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    return render_template('logout.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already exists')
        return redirect(url_for('auth.signup'))
    else:
        new_user = User(email = email, name = name, password = password)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('name') else False

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Please check your login details and try again!')
        return redirect(url_for('auth.login'))
    else:
        if user.password == password:
            return redirect(url_for('main.profile'))
        flash('Incorrect Email or Password!!')
        return redirect(url_for('auth.login'))

