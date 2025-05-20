from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_login import current_user
from flask import Flask

auth = Blueprint('auth', __name__)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

class Admin(UserMixin):
    id = "1"
    username = "admin"
    password = "admin"

@login_manager.user_loader
def load_user(user_id):
    return Admin() if user_id == "1" else None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == Admin.username and request.form['password'] == Admin.password:
            login_user(Admin())
            return redirect(url_for('index'))
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
