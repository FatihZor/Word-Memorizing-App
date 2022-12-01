from flask_login import login_user, logout_user, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db, login_manager
from app.config import Config

from app.auth.models import User

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None

@auth.route('/login',
            methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_ = request.args.get('next')
            return redirect(next_ or url_for('main.index'))
        else:
            flash('Informations incorrect', category='error')
    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have logged out now.', category='info')
    return redirect(url_for('auth.login'))


@auth.route('/register',
            methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username=username,
                    password=password)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, register success. You can log in now.', category='success')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html')

