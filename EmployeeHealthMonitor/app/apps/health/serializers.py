from app.extensions import ma
from ..health.models import HealthData

class HealthDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HealthData
        load_instance = True
        include_fk = True