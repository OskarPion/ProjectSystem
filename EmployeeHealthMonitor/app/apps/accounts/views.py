from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from ..accounts.models import User
from ..employees.models import Employee
from ..health.models import HealthData

from ..accounts.serializers import UserSchema
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, date

accounts_bp = Blueprint('accounts', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@accounts_bp.route('/profile')
@login_required
def profile():
    # Получаем последние медицинские данные сотрудника
    health_data = None
    if current_user.employee:
        health_data = HealthData.query.filter_by(employee_id=current_user.employee.id).first()
    
    return render_template('profile.html', 
                         user=current_user,
                         health_data=health_data)

@accounts_bp.route('/auth')
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('health.dashboard'))
    return render_template('login.html')

@accounts_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('health.dashboard'))
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        flash('Неверное имя пользователя или пароль', 'error')
        return redirect(url_for('accounts.auth'))
    
    login_user(user)
    flash('Вы успешно вошли в систему!', 'success')
    return redirect(url_for('health.dashboard'))

@accounts_bp.route('/register', methods=['POST'])
def register():
    try:
        # Получаем данные формы
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        birth_date_str = request.form.get('birth_date')
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        
        # Валидация
        if birth_date:
            min_date = date(1900, 1, 1)
            max_date = date.today()
            if birth_date < min_date or birth_date > max_date:
                flash('Некорректная дата рождения', 'error')
                return redirect(url_for('accounts.auth'))

        if not all([last_name, first_name, email, password, password_confirm]):
            flash('Все обязательные поля должны быть заполнены', 'error')
            return redirect(url_for('accounts.auth'))

        if password != password_confirm:
            flash('Пароли не совпадают', 'error')
            return redirect(url_for('accounts.auth'))

        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'error')
            return redirect(url_for('accounts.auth'))

        # Создание пользователя
        new_user = User(
            last_name=request.form['last_name'],
            first_name=request.form['first_name'],
            middle_name=request.form.get('middle_name'),
            email=request.form['email'],
            password_hash=generate_password_hash(request.form['password']),
            birth_date=birth_date,
            is_admin=False
        )
        
        db.session.add(new_user)
        db.session.flush()
        
        full_name = f"{last_name} {first_name} {middle_name or ''}".strip()
        # Создаем запись сотрудника
        new_employee = Employee(
            user_id=new_user.id,
            name=full_name,
            position="Новый сотрудник",
            hire_date=datetime.now().date()
        )
        
        db.session.add(new_employee)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('accounts.auth'))

    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка регистрации: {str(e)}', 'error')
        return redirect(url_for('accounts.auth'))

@accounts_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('accounts.auth'))
