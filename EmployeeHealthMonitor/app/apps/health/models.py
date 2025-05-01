from app.extensions import db
from datetime import datetime

class HealthData(db.Model):
    __tablename__ = 'health_data'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    employee = db.relationship('Employee', back_populates='health_records')
    date = db.Column(db.Date, default=datetime.now)

    # Основные медицинские данные
    gender = db.Column(db.String(10))         # Пол (M/Ж)
    height = db.Column(db.Integer)            # Рост (см)
    weight = db.Column(db.Float)              # Вес (кг)
    temperature = db.Column(db.Float)         # Температура (°C)
    systolic = db.Column(db.Integer)          # Систолическое давление
    diastolic = db.Column(db.Integer)         # Диастолическое давление
    heart_rate = db.Column(db.Integer)        # Пульс
    blood_oxygen = db.Column(db.Integer)      # Уровень кислорода в крови (%)
    bmi = db.Column(db.Float)                 # Индекс массы тела

    def __repr__(self):
        return f'<HealthData {self.employee_id} {self.date}>'
