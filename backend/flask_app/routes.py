from flask import Blueprint, render_template, request, redirect, jsonify
from models import get_all_users, create_user

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/')
def index():
    users = get_all_users()
    return render_template('index.html', users=users)

@routes_blueprint.route('/create-user', methods=['POST'])
def create():
    name = request.form['name']
    email = request.form['email']
    balance = request.form['balance']
    create_user(name, email, balance)
    return redirect('/')
