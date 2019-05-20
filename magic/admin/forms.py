from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, DateField, IntegerField, HiddenField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_wtf.file import FileField, FileAllowed 
from magic.models import * 

 
class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    category = SelectField('Select Category',choices=[('funny', 'Funny'),('lifestyle', 'Lifestyle'),('inspire', 'Inspire'),('animation', 'Animation')], validators=[DataRequired()])
    short_description = TextAreaField('Short Description', validators=[DataRequired()])
    thumbnail = FileField('Upload Video Thumbnail', validators=[FileAllowed(['jpg','png'])])
    video = FileField('Upload Video File', validators=[FileAllowed(['mp4','3gp'])])
    submit = SubmitField('Upload')

class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    short_description = TextAreaField('Short Description', validators=[DataRequired()])
    submit = SubmitField('Update')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CreateAdminForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Choose Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role',choices=[('admin', 'Administrator'),('editor', 'Editor')], validators=[DataRequired()])
    thumbnail = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data).first()
        if admin:
            raise ValidationError('Admin already exists!!')



class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email')

    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data).first()
        if admin is None:
            raise ValidationError('There is no account with that email, you are not an admin !')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')