from flask import Blueprint, request, jsonify
from app.extensions import db
from ..health.models import HealthData
from ..health.serializers import HealthDataSchema
from flask_login import login_required

health_bp = Blueprint('health', __name__)
health_schema = HealthDataSchema()
healths_schema = HealthDataSchema(many=True)

@health_bp.route('/', methods=['GET'])
@login_required
def list_health():
    records = HealthData.query.all()
    return healths_schema.jsonify(records)

@health_bp.route('/', methods=['POST'])
@login_required
def create_health():
    data = request.json
    rec = HealthData(**data)
    db.session.add(rec)
    db.session.commit()