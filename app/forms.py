from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField # wtforms html5 contains pop up calendar display
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from app.models import User

''' Login Form includes required fields of username and password, an optional remember me check box, and a submit button. '''
class LoginForm(FlaskForm):
    username = StringField('Username or E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

''' Registration Form includes required fields of username, email, password, and password confirmation, and a submit button. '''
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    ''' Custom Validators: 'validate_<field_name>' '''

    # Ensure username is not already registered.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # Ensure email is not already registered.
    def validate_email(self, email):
        mail = User.query.filter_by(email=email.data).first()
        if mail is not None:
            raise ValidationError('Please use a different email address.')

''' To-Do Task Form includes a field to input a task and a submit button. '''
class TaskForm(FlaskForm):
    task = TextAreaField('Add Task', validators=[Length(max=140)])
    submit = SubmitField('Submit')

''' Due Date Form includes a field to input a due date and a submit button. '''
class DueDateForm(FlaskForm):
    ''' The DateField generates a pop up calendar which the user can select a date from or manually enter a date. This date gets sent as a POST request as a datetime.date object in the form 'YYYY-MM-DD'. If a user manually enters a date I expect it to be in the form MM/DD/YYYY, so the format argument will get the user input MM/DD/YYYY and set it to YYYY-MM-DD before the POST request to avoid errors. '''
    due_date = DateField('Enter Due Date:', format='%Y-%m-%d')
    submit = SubmitField('Submit')
