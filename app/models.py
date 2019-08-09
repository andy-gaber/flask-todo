from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # tasks references the class Task with 'Task', User is the one to many Tasks
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    list_as_descending = db.Column(db.Boolean)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def tasks_descending(self):
        ''' This is a Task object, in routes.py when this function is called it will return an object, so in order to get the list of tasks the route will call all_tasks().all(), which is an SQL function that return the items as a List'''
        user_tasks = Task.query.filter_by(user_id=self.id)
        return user_tasks.order_by(Task.timestamp.desc())

    def tasks_ascending(self):
        ''' This is a Task object, in routes.py when this function is called it will return an object, so in order to get the list of tasks the route will call all_tasks().all(), which is an SQL function that return the items as a List'''
        user_tasks = Task.query.filter_by(user_id=self.id)
        return user_tasks.order_by(Task.timestamp)

'''
To-do tasks for a user
timestamp is indexed to efficiently retreive todos in chronologucal order
'''

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user.id: 'user' is the table name (SQLAlchemy automatically uses lowercase
    # and snake case for model names)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Task {self.body}>'

# if doesnt work change user_id to id
''' This callback is used to reload the user object from the user ID stored in the session. It should take the unicode ID of a user, and return the corresponding user object. It should return None (not raise an exception) if the ID is not valid. (In that case, the ID will manually be removed from the session and processing will continue.)'''


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

