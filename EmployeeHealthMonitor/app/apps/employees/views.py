from flask import Blueprint, request, jsonify
from app.extensions import db
from ..employees.models import Employee
from ..employees.serializers import EmployeeSchema
from flask_login import login_required

employees_bp = Blueprint('employees', __name__)
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

@employees_bp.route('/', methods=['GET'])
@login_required
def list_employees():
    employees = Employee.query.all()
    return employees_schema.jsonify(employees)

@employees_bp.route('/', methods=['POST'])
@login_required
def create_employee():
    data = request.json
    emp = Employee(**data)
    db.session.add(emp)
    db.session.commit()
    return employee_schema.jsonify(emp), 201