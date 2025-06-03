from EmployeeHealthMonitor.app.extensions import db

class HealthData(db.Model):
    __tablename__ = 'health_data'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    systolic = db.Column(db.Integer)     # Систолическое давление
    diastolic = db.Column(db.Integer)    # Диастолическое давление
    heart_rate = db.Column(db.Integer)   # Пульс
    steps = db.Column(db.Integer)        # Количество шагов (НУЖНО ДОБАВИТЬ!!!)

    def __repr__(self):
        return f'<HealthData {self.employee_id} {self.date}>'
