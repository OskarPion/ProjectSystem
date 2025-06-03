import flask

from flask import Blueprint, request, jsonify
from EmployeeHealthMonitor.app.extensions import db
from ..reports.models import Report
from ..reports.serializers import ReportSchema
from flask_login import login_required

reports_bp = Blueprint('reports', __name__)
report_schema = ReportSchema()
reports_schema = ReportSchema(many=True)

@reports_bp.route('/', methods=['GET'])
@login_required
def list_reports():
    rep = Report.query.all()
    return reports_schema.jsonify(rep)

@reports_bp.route('/', methods=['POST'])
@login_required
def create_report():
    data = request.json
    r = Report(**data)
    db.session.add(r)
    db.session.commit()
    return report_schema.jsonify(r), 201