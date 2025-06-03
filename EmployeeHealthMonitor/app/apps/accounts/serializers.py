from EmployeeHealthMonitor.app.extensions import ma
from ..accounts.models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True