import datetime
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, TaskForm, DueDateForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Task
''' Flask-Login contains the 'current_user' proxy, which interfaces with the database, so when 'current_user' is called the return is the current User class user object that is logged in. '''

# Index (Home Page) Route Function
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # If viewing app as an anonymous user the user is shown default welcome page.
    if current_user.is_anonymous:
        return render_template('index.html', title='Home')

    form = TaskForm()
    # If TaskForm is submitted and validated a new task is added to user's to-do list.
    if form.validate_on_submit():
        task = Task(body=form.task.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash(f'You added a to-do task, {current_user.username} ')
        ''' Redirect to index after POST request generated by a web form submission to avoid sumbitting duplicate posts. '''
        return redirect(url_for('index'))

    # Get user's sorting preference for their tasks to display in HTML template.
    user = User.query.filter_by(id=current_user.id).first()
    tasks = user.get_sorted_view_of_tasks()

    # Render personal index page.
    return render_template('index.html', title='Home', form=form, tasks=tasks)

# Login Route Function
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in but navigates to /login URL redirect to index page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # If LoginForm is submitted and validated, check username and password and login user if authenticated.
    if form.validate_on_submit():
        ''' The user can log in with their username or email address. The 'username' and 'email' variables are database User model objects which are set by a database search of a user's username or email, whichever the user inputs to log in. '''
        username = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.username.data).first()

        # Check username (or email) and password, if one or both are invalid flash error message and redirect to /login.
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

        # if user is authenticated and logged in, redirect to /index.
        return redirect(url_for('index'))

    # If there is an error with form submission render default login page.
    return render_template('login.html', title='Sign In', form=form)

# Logout Route Function
@app.route('/logout')
def logout():
    # Call Flask-Login's logout_user function.
    logout_user()
    return redirect(url_for('index'))

# Register Account Route Function
@app.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already registered but navigates to /register URL redirect to index page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    # If RegistrationForm is submitted and validated created new user model in database.
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        # Redirect newly registered user to login page.
        return redirect(url_for('login'))

    # If form not validated, render again registration page.
    return render_template('register.html', title='Register', form=form)

# Delete Task Route Function. Dynamic 'task_id' is passed via GET request.
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    # The unique task the user chose to delete, based on dynamic 'task_id'.
    task = Task.query.filter_by(id=int(task_id)).first()
    # If error occurs while searching database for task, redirect to index.
    if task is None:
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    flash(f'Task Deleted')
    return redirect(url_for('index'))

# Sort User Tasks By Newest Route Function
@app.route('/newest')
def newest():
    ''' Set user model boolean variables to sort tasks by user's selected preference. Here user chose to view by newest tasks first. '''
    user = User.query.filter_by(id=current_user.id).first()
    user.set_sorted_view_of_tasks(view_by_newest=True, view_by_oldest=False, view_by_due_date=False)

    db.session.commit()

    return redirect(url_for('index'))

# Sort User Tasks By Oldest Route Function
@app.route('/oldest')
def oldest():
    ''' Set user model boolean variables to sort tasks by user's selected preference. Here user chose to view by oldest tasks first. '''
    user = User.query.filter_by(id=current_user.id).first()
    user.set_sorted_view_of_tasks(view_by_newest=False, view_by_oldest=True, view_by_due_date=False)

    db.session.commit()

    return redirect(url_for('index'))

# Sort User Tasks By Due Date Route Function
@app.route('/view_by_due_date')
def view_by_due_date():
    ''' Set user model boolean variables to sort tasks by user's selected preference. Here user chose to view by due date (earliest first). '''
    user = User.query.filter_by(id=current_user.id).first()
    user.set_sorted_view_of_tasks(view_by_newest=False, view_by_oldest=False, view_by_due_date=True)

    db.session.commit()

    return redirect(url_for('index'))

# Set Due Date Route Function. Dynamic 'task_id' is passed via GET request.
@app.route('/set_due_date/<task_id>', methods=['GET', 'POST'])
def set_due_date(task_id):
    # If viewing app as an anonymous user the user is shown default welcome page.
    if current_user.is_anonymous:
        return render_template('index.html', title='Home')

    form = DueDateForm()
    ''' If DueDateForm is submitted and validated create a due date for the unique task the user chose, based on dynamic 'task_id'. '''
    if form.validate_on_submit():
        # The unique task the user chose to add a due date, based on dynamic 'task_id'.
        task = Task.query.filter_by(id=int(task_id)).first()
        # If error occurs while searching database for task, redirect to index.
        if task is None:
            return redirect(url_for('index'))

        ''' Flask request.form is a dictionary lookup, it returns a value that corresponds to the lookup key. Here the key is the HTML 'name' attribute, and the value it returns is the HTML 'value' attribute. For example, a user will input a due date of 12/01/2020 and the element will show:

        <input id="due_date" name="due_date" type="text" value="12/01/2020">

        The attributes name="due_date", and value="12/01/2020" are the key and values for this request. The user input due date will be set to the variable 'date'. '''
        date = request.form['due_date']

        ''' User selects due date via popup calendar that displays MM/DD/YYYY, but entry date sent in POST is 'YYYY-MM-DD'. Grab the date by flask request, separate the year, month, and date, and set these parameters in a datetime.date object, and set this datetime.date as the task due date in the Task model. '''
        year, month, day = date.split('-')
        due_date = datetime.date(year=int(year), month=int(month), day=int(day))

        task.set_due_date(due_date)
        db.session.add(task)
        db.session.commit()
        flash(f'Due Date Set For {month}/{day}/{year}')
        # Redirect to users personal to-do list.
        return redirect(url_for('index'))

    # If form is not vaidated, render again due date page.
    return render_template('due_date.html', title='Set Due Date', form=form)

# Remove Due Date Route Function. Dynamic 'task_id' is passed via GET request.
@app.route('/remove_due_date/<task_id>')
def remove_due_date(task_id):
    # The unique task the user chose to remove a due date, based on dynamic 'task_id'.
    task = Task.query.filter_by(id=int(task_id)).first()
    # If error occurs while searching database for task, redirect to index.
    if task is None:
        return redirect(url_for('index'))

    # Set Task model due_date variable to None, i.e. remove current due date.
    due_date = None
    task.set_due_date(due_date)
    db.session.add(task)
    db.session.commit()
    flash(f'Due Date Removed')
    # Redirect to users personal to-do list.
    return redirect(url_for('index'))
