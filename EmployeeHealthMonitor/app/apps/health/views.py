from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from app.extensions import db
from ..health.models import HealthData
from ..employees.models import Employee
from ..health.serializers import HealthDataSchema
from flask_login import login_required, current_user
from datetime import datetime
from sqlalchemy.orm import joinedload

health_bp = Blueprint('health', __name__)
health_schema = HealthDataSchema()
healths_schema = HealthDataSchema(many=True)

@health_bp.route('/add_data', methods=['GET', 'POST'])
@login_required
def add_data():
    # Получаем текущего сотрудника
    employee = current_user.employee
    if not employee:
        flash('Сотрудник не найден', 'error')
        return redirect(url_for('health.dashboard'))

    # Получаем существующие данные (если есть)
    health_data = HealthData.query.filter_by(employee_id=employee.id).first()

    if request.method == 'POST':
        try:
            if health_data:
                # Обновляем существующую запись
                health_data.gender = request.form.get('gender')
                health_data.height = float(request.form.get('height'))
                health_data.weight = float(request.form.get('weight'))
                health_data.temperature = float(request.form.get('temperature'))
                health_data.systolic = int(request.form.get('systolic'))
                health_data.diastolic = int(request.form.get('diastolic'))
                health_data.heart_rate = int(request.form.get('heart_rate'))
                health_data.blood_oxygen = int(request.form.get('blood_oxygen'))
                health_data.bmi = float(request.form.get('bmi'))
                health_data.date = datetime.now().date()
                flash('Данные успешно обновлены', 'success')
            else:
                # Создаем новую запись
                health_data = HealthData(
                    employee_id=employee.id,
                    gender=request.form.get('gender'),
                    height=float(request.form.get('height')),
                    weight=float(request.form.get('weight')),
                    temperature=float(request.form.get('temperature')),
                    systolic=int(request.form.get('systolic')),
                    diastolic=int(request.form.get('diastolic')),
                    heart_rate=int(request.form.get('heart_rate')),
                    blood_oxygen=int(request.form.get('blood_oxygen')),
                    bmi=float(request.form.get('bmi')),
                    date=datetime.now().date()
                )
                db.session.add(health_data)
                flash('Данные успешно сохранены', 'success')
            
            db.session.commit()
            return redirect(url_for('health.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при сохранении данных: {str(e)}', 'error')

    return render_template('add_data.html', health_data=health_data)

@health_bp.route('/dashboard')
@login_required
def dashboard():
    employees = Employee.query.options(
        joinedload(Employee.user),
        joinedload(Employee.health_records)
    ).all()
    return render_template('dashboard.html', employees=employees)