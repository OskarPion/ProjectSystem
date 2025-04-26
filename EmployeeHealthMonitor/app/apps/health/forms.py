from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired

class HealthDataForm(FlaskForm):
    employee_id = IntegerField('Employee ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    systolic = IntegerField('Systolic Pressure', validators=[DataRequired()])
    diastolic = IntegerField('Diastolic Pressure', validators=[DataRequired()])
    heart_rate = IntegerField('Heart Rate', validators=[DataRequired()])
    submit = SubmitField('Submit')