from app.extensions import ma
from ..reports.models import Report

class ReportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Report
        load_instance = True
        include_fk = True