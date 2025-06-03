from flask import Blueprint, request, jsonify
from ..analytics.ml_models import DiseaseRiskModel

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json.get('features')
    model = DiseaseRiskModel()
    risk = model.predict([data])[0]
    return jsonify({'risk': risk})