import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ''' SECRET_KEY used by Flask-WTF to protect app web forms against Cross-Site Request Forgery (CSRF) attacks. Set it to environment variable, or if not defined set to this randomly generated string. '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4131108e4aa3eeff7c1c41d58455f6a6'

    # Debugging Database: SQLite
    # Deployment Database: Heroku's Postgresql
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    ''' The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False to disable a feature of Flask-SQLAlchemy not needed, which is to signal the application every time a change is about to be made in the database. '''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
