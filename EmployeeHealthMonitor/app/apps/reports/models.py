# app/apps/reports/models.py

from app.extensions import db
from app.core.models import Disease   # ВАЖНО! Импортируем Disease до Report

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())

    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.id'), nullable=True)
    disease = db.relationship('Disease', back_populates='reports')

    def __repr__(self):
        return f'<Report {self.title}>'
