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
    view_tasks_by_newest = db.Column(db.Boolean, default=True)
    view_tasks_by_oldest = db.Column(db.Boolean, default=False)
    view_tasks_by_due_date = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_sorted_view_of_tasks(self):
        # user_tasks is Task object
        # all() converts to List
        user_tasks = Task.query.filter_by(user_id=self.id)
        if self.view_tasks_by_newest:
            return user_tasks.order_by(Task.timestamp.desc()).all()
        elif self.view_tasks_by_oldest:
            return user_tasks.order_by(Task.timestamp).all()
        elif self.view_tasks_by_due_date:
            ''' Here the user selected to view tasks by due date, which will display tasks in the order they are due, starting with the earliest due date. When a Task is instantiated the due_date field is set to None by default, and None is less than any datetime.date, so when the tasks are sorted by the database the tasks with due dates equal to None are displayed before the tasks with actual due dates. To correct this, when the list of tasks is queried a custom sorting algorithm is used to shuffle all the tasks with due dates to the front of the list and push all the tasks with None due dates to the end of the list. In-place, linear sort. '''

            tasks = user_tasks.order_by(Task.due_date).all() # here tasks is unsorted list
            left = 0
            right = 0
            ''' start with left and right variables at first index of list, traverse with right as leader and left as follower until right reaches a task with a due date, then swap left with right and continue until right reaches the end of the list '''
            while right < len(tasks):
                if tasks[right].due_date == None:
                    right += 1
                else:
                    tasks[left], tasks[right] = tasks[right], tasks[left]
                    left += 1
                    right += 1
            return tasks

    def set_sorted_view_of_tasks(self, view_by_newest, view_by_oldest, view_by_due_date):
        if view_by_newest:
            self.view_tasks_by_newest = True
            self.view_tasks_by_oldest = False
            self.view_tasks_by_due_date = False
        elif view_by_oldest:
            self.view_tasks_by_oldest = True
            self.view_tasks_by_newest = False
            self.view_tasks_by_due_date = False
        elif view_by_due_date:
            self.view_tasks_by_due_date = True
            self.view_tasks_by_newest = False
            self.view_tasks_by_oldest = False

''' OLD GETTER
    def tasks_descending(self):
        user_tasks = Task.query.filter_by(user_id=self.id)
        return user_tasks.order_by(Task.timestamp.desc())

    def tasks_ascending(self):
        user_tasks = Task.query.filter_by(user_id=self.id)
        return user_tasks.order_by(Task.timestamp)

    def order_by_due_date(self):
        user_tasks = Task.query.filter_by(user_id=self.id)
        return user_tasks.order_by(Task.due_date.desc())
'''

'''
To-do tasks for a user
timestamp is indexed to efficiently retrieve todos in chronologucal order
'''
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user.id: 'user' is the table name (SQLAlchemy automatically uses lowercase and snake case for model names)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    due_date = db.Column(db.Date, index=True)

    def __repr__(self):
        return f'<Task {self.body}>'

    def set_due_date(self, date):
        self.due_date = date


''' This callback is used to reload the user object from the user ID stored in the session. It should take the unicode ID of a user, and return the corresponding user object. It should return None (not raise an exception) if the ID is not valid. (In that case, the ID will manually be removed from the session and processing will continue.)'''
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

