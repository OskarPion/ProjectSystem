from EmployeeHealthMonitor.app.extensions import celery, db
from EmployeeHealthMonitor.app.apps.analytics.ml_models import DiseaseRiskModel
from EmployeeHealthMonitor.app.apps.health.models import HealthData

@celery.task()
def train_risk_model():
    records = HealthData.query.all()
    X = [[rec.systolic, rec.diastolic, rec.heart_rate] for rec in records]
    y = [0 for _ in records]
    model = DiseaseRiskModel()
    model.train(X, y)
    return 'trained'