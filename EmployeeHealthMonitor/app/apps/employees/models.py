from EmployeeHealthMonitor.app.extensions import db

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(100))
    hire_date = db.Column(db.Date)
    user = db.relationship('User', backref='employees')

    def __repr__(self):
        return f'<Employee {self.name}>'