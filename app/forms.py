from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    ''' custom validators that match pattern 'validate_<field_name>' are recognized by WTForms and are invoked on variables that are <field_name>, in this case username and email from this class RegistrationForm.    '''

    # ensure username is not already registered
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # ensure email is not already registered
    def validate_email(self, email):
        mail = User.query.filter_by(email=email.data).first()
        if mail is not None:
            raise ValidationError('Please use a different email address.')

class TaskForm(FlaskForm):
    task = TextAreaField('Add Task', validators=[Length(max=140)])
    submit = SubmitField('Submit')

