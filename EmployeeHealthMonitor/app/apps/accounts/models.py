from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)  # Фамилия
    first_name = db.Column(db.String(100), nullable=False)  # Имя
    middle_name = db.Column(db.String(100))  # Отчество (необязательное)
    is_admin = db.Column(db.Boolean, default=False)
    birth_date = db.Column(db.Date)

    employee = db.relationship('Employee', back_populates='user', uselist=False)
    
    def __repr__(self):
        return f'<User {self.last_name} {self.first_name}>'