from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from webapp.models import *


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=32)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm password',
                                          validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.select().where(User.username == username.data).exists():
            raise ValidationError("Username '" + username.data + "' already in use")

    def validate_email(self, email):
        if User.select().where(User.email == email.data).exists():
            raise ValidationError("Email '" + email.data + "' already in use")


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=32)])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Log in')


'''
class TaskAddForm(FlaskForm):
    title = StringField('Task title',
                       validators=[DataRequired(), Length(min=1, max=64)])
    maxpoints = IntegerField('Maximum points', validators=[NumberRange(min=1)])
    text = FileField('File with task text', validators=[FileAllowed(['pdf', 'txt', ''])])
    public = BooleanField('Public')
    submit = SubmitField('Add task')
'''


class CompetitionAddForm(FlaskForm):
    name = StringField('Competition name',
                       validators=[DataRequired(), Length(min=1, max=64)])
    start_time = DateTimeField('Start time', [DataRequired()])
    end_time = DateTimeField('End time', [DataRequired()])
    public = BooleanField('Public')
    submit = SubmitField('Add competition')

    def validate_start_time(self, start_time):
        if start_time.data < datetime.now():
            raise ValidationError('Start time must be after now')

    def validate_end_time(self, end_time):
        if end_time.data < start_time.data:
            raise ValidationError('End time must be after start time')
