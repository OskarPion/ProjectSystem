from flask import Blueprint, request, jsonify, render_template
from ..analytics.ml_models import DiseaseRiskModel

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/health_chart')
def health_chart():
    return render_template('health_chart.html')

@analytics_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json.get('features')
    model = DiseaseRiskModel()
    risk = model.predict([data])[0]
    return jsonify({'risk': risk})