from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, BooleanField, IntegerField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from webapp.models import User, Competition, Task, Language
from datetime import datetime
import zipfile


class NotValidatedSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        pass

class NotValidatedSelectField(SelectField):
    def pre_validate(self, form):
        pass


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

    def validate_username(self, username):
        if not User.select().where(User.username == username.data).exists():
            raise ValidationError("Username '" + username.data + "' does not exist")


class TaskAddForm(FlaskForm):
    title = StringField('Task title',
                       validators=[DataRequired(), Length(min=1, max=64)])
    text = FileField('File with task text (.pdf or .txt)',
                     validators=[FileAllowed(['pdf', 'txt']), DataRequired()])
    maxpoints = IntegerField('Maximum points',
                             validators=[DataRequired(), NumberRange(min=1)])
    tests = FileField('A zip archive of tsts ang expected outputs',
                      validators=[FileAllowed(['zip']), DataRequired()])
    public = BooleanField('Public')
    submit = SubmitField('Add task')

    def validate_title(self, title):
        if Task.select().where(Task.title == title.data).exists():
            raise ValidationError("Task '" + title.data + "' already exist")

    def validate_tests(self, tests):
        pass            #TODO


#class TaskEditForm(TaskAddForm):       #TODO
#    submit = SubmitField('Update task info')


class CompetitionAddForm(FlaskForm):
    name = StringField('Competition name',
                       validators=[DataRequired(), Length(min=1, max=64)])
    start_time = DateTimeField('Start time', validators=[DataRequired()], format="%d.%m.%Y %H:%M")
    end_time = DateTimeField('End time', validators=[DataRequired()], format="%d.%m.%Y %H:%M")
    public = BooleanField('Public:')
    tasks = NotValidatedSelectMultipleField('Tasks', choices=[(t.id, t.title) for t in Task.select()])
    submit = SubmitField('Add competition')

    def validate_start_time(self, start_time):
        if start_time.data < datetime.now():
            raise ValidationError('Start time must be in the future')

    def validate_end_time(self, end_time):
        if end_time.data <= self.start_time.data:
            raise ValidationError('End time must be after start time')

    def validate_name(self, name):
        if Competition.select().where(Competition.name == name.data).exists():
            raise ValidationError("Competition '" + name.data + "' already exist")

class TaskSubmitForm(FlaskForm):
    code = FileField('Source code', validators=[DataRequired()])
    language = NotValidatedSelectField('Programming language', choices=[(l.id, l.name) for l in Language.select()], validators=[DataRequired()])
    submit = SubmitField('Submit solution')

