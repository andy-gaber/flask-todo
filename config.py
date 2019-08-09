import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Generate random characters: In Terminal: python, import secrets, secrets.token_hex(16)
    ''' The Flask-WTF extension uses it to protect web forms against a nasty attack called Cross-Site Request Forgery or CSRF. A value sourced from an environment variable is preferred, but if the environment does not define the variable, then the hardcoded string is used instead.'''
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4131108e4aa3eeff7c1c41d58455f6a6'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    ''' The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False to disable a feature of Flask-SQLAlchemy that I do not need, which is to signal the application every time a change is about to be made in the database '''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
