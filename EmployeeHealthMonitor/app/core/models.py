# app/core/models.py

from EmployeeHealthMonitor.app.extensions import db

class Disease(db.Model):
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)

    # Правильная связь с Report
    reports = db.relationship('Report', back_populates='disease', lazy=True)

    def __repr__(self):
        return f'<Disease {self.name}>'
