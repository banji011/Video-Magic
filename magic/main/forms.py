from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, DateField, IntegerField, HiddenField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_wtf.file import FileField, FileAllowed 

 

class LoginForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired(),Length(min=2, max=30)])
    network = SelectField('Network',choices=[('mtn', 'MTN'),('airtel', 'Airtel'),('9mobile', '9mobile')], validators=[DataRequired()])
    submit = SubmitField('Login')