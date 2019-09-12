import datetime
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, TaskForm, DueDateForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Task
'''
url_for('login') returns /login, and url_for('index') return '/index. The argument to url_for() is the endpoint name, which is the name of the view function
'''
'''
current_user is function of flask_login libray, which interfaces with database, so when current_user is called the return is the current User class user that is logged in. Similar to calling td = User.tasks_descending()
'''
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    ''' if anonymous user is shown generic welcome page that asks user to register or sign in to use app'''
    if current_user.is_anonymous:
        return render_template('index.html', title='Home')
    ''' else, user is logged in and show users to-do list page with form to add task and list of to-dos '''
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(body=form.task.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash(f'You added a to-do task, {current_user.username} ')
        # respond to a POST request generated by a web form submission
        # with a redirect: Post/Redirect/Get patttern, to avoid inserting
        # duplicate posts... https://en.wikipedia.org/wiki/Post/Redirect/Get
        return redirect(url_for('index'))

    user = User.query.filter_by(id=current_user.id).first()
    tasks = user.get_sorted_view_of_tasks()

    return render_template('index.html', title='Home', form=form, tasks=tasks)




@app.route('/login', methods=['GET', 'POST'])
def login():
    # user already logged in, but navigates to /login URL, if this
    # happens redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        ''' user can log in by their username or email address. The 'username' and 'email' variables are database User objects which are set by a database search of a User by their username or email, whichever the user inputs to log in '''
        username = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.username.data).first()

        ''' Check username and password, if one or both are invalid flash error message and redirect to /login. Do not inform user that it is their username or password or both that are invalid, only that the login credentials are invalid - security issue '''
        if username:
            if not username.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
        elif email:
            if not email.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

        ''' By default, when the user closes their browser the Flask Session is deleted and the user is logged out. “Remember Me” prevents the user from accidentally being logged out when they close their browser. '''
        if username:
            login_user(username, remember=form.remember_me.data)
        elif email:
            login_user(email, remember=form.remember_me.data)
        # if user is authenticated and logged in, redirect to /index
        return redirect(url_for('index'))

    # error with form, not valid for some reason, display /login page
    # to try again (note: return render_template, not redirect
    return render_template('login.html', title='Sign In', form=form)




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    task = Task.query.filter_by(id=int(task_id)).first()
    if task is None:
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    flash(f'Task: {task_id} Deleted')
    return redirect(url_for('index'))

# Descending Tasks
@app.route('/newest')
def newest():
    user = User.query.filter_by(id=current_user.id).first()
    user.set_sorted_view_of_tasks(view_by_newest=True, view_by_oldest=False, view_by_due_date=False)

    db.session.commit()

    flash(f'Descending Tasks')
    return redirect(url_for('index'))

# Ascending Tasks
@app.route('/oldest')
def oldest():
    user = User.query.filter_by(id=current_user.id).first()
    user.set_sorted_view_of_tasks(view_by_newest=False, view_by_oldest=True, view_by_due_date=False)

    db.session.commit()

    flash(f'Ascending Tasks')
    return redirect(url_for('index'))

# Descending Tasks By Due Date
@app.route('/view_by_due_date')
def view_by_due_date():
    user = User.query.filter_by(id=current_user.id).first()
    user.set_sorted_view_of_tasks(view_by_newest=False, view_by_oldest=False, view_by_due_date=True)

    db.session.commit()

    flash(f'List By Due Date')
    return redirect(url_for('index'))

@app.route('/set_due_date/<task_id>', methods=['GET', 'POST'])
def set_due_date(task_id):
    if current_user.is_anonymous:
        return render_template('index.html', title='Home')
    form = DueDateForm()
    if form.validate_on_submit():
        task = Task.query.filter_by(id=int(task_id)).first()
        if task is None:
            return redirect(url_for('index'))
        # html form {key : vaule} -> {'due_date' : '<user input date>'}
        # EX: <input id="due_date" name="due_date" type="text" value="01/03/2004">
        date = request.form['due_date']
        print(form.due_date)
        print(date)
        ''' User selects due date via popup calendar that displays MM/DD/YYYY, but entry date sent in POST is 'YYYY-MM-DD'. Grab the date by flask request, separate the year, month, date, set these parameters in a datetime.date object, and set this datetime.date as the task due date in Task model  '''
        year, month, day = date.split('-')
        print(year, month, day)

        due_date = datetime.date(year=int(year), month=int(month), day=int(day))
        print(due_date)
        print(type(due_date))

        task.set_due_date(due_date)
        db.session.add(task)
        db.session.commit()
        flash(f'Due Date Set For {month}/{day}/{year}')
        return redirect(url_for('index'))
    return render_template('due_date.html', title='Set Due Date', form=form)

@app.route('/remove_due_date/<task_id>')
def remove_due_date(task_id):

    task = Task.query.filter_by(id=int(task_id)).first()
    if task is None:
        return redirect(url_for('index'))

    due_date = None
    task.set_due_date(due_date)
    db.session.add(task)

    db.session.commit()

    flash(f'Due Date Removed')
    return redirect(url_for('index'))
