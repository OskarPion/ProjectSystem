from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from ..accounts.models import User
from ..accounts.serializers import UserSchema
from flask_login import login_user, logout_user, login_required

accounts_bp = Blueprint('accounts', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@accounts_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed = generate_password_hash(data['password'])
    user = User(username=data['username'], email=data['email'], password_hash=hashed)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

@accounts_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first_or_404()
    if check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return user_schema.jsonify(user)
    return jsonify({'error': 'Invalid credentials'}), 401

@accounts_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})