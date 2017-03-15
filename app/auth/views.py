from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app import db
from app.auth import auth as auth_bl
from app.auth.forms import LoginForm, RegisterForm
from app.models import User

BAD_CREDENTIALS = 'Wrong login or password'
JUST_REGISTERED = 'You have just registered, please log in'
LOGIN_PROBLEM = 'There\'s been some problem with login'
REGISTRATION_FAILURE = 'The registration has failed'
WELCOME = 'Welcome!'


@auth_bl.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User.from_json({'email': form.data.get('email'), 'password': form.data.get('password')})
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            print(ex)
            flash(REGISTRATION_FAILURE)
        else:
            flash(JUST_REGISTERED)
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bl.route('/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()

    if form.validate_on_submit():
        email = form.data.get('email')
        password = form.data.get('password')
        try:
            user = User.query.filter_by(email=email).first()
            if user and user.verify_password(password) and user.is_active:
                    login_user(user)
                    flash(WELCOME)
                    return redirect(url_for('main.dashboard'))
            else:
                flash(BAD_CREDENTIALS)
        except Exception as ex:
            print(ex)
            flash(LOGIN_PROBLEM)
    return render_template('auth/login.html', form=form)


@auth_bl.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




