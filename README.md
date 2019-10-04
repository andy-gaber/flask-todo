https://to-do-flask.herokuapp.com

This web application allows users to register an account to make a personal to-do list. Users can create a username and password, log in, add tasks, add/remove due dates for tasks, sort their tasks by newest, oldest, or due date, and delete completed tasks. 

The app was created with Flask, a micro web application framework. Web forms are generated with the Flask-WTF extension, a WTForms wrapper. Users are able to fill out a registration form for an account, fill in a log in form to log into their account, add new tasks in a task form, and add due dates to tasks using a due date form. The web template engine Jinja2 was used to generate the app’s custom web pages and to incorporate static and dynamic elements. 

Persistent data storage is managed using the SQLAlchemy Python library. A user model stores each unique user’s id, username, email address, hashed password, and personal tasks; and a task model stores each unique task and its metadata including task id, timestamp, the user’s id relationship, and task due date. SQLite was used during development, and Heroku’s PostgreSQL is used for deployment.

View functions route the GET and POST requests to their specified web pages. The index view function will render a default homepage for any visiting user not logged in. A user can then navigate to the register view function, and then the login view function, which route to the registration and login forms, respectively. When a user logs in they will be directed to their personal homepage that displays their to-do list. There are also view functions that route users to various web pages and web forms, such as setting a due date, removing a due date, sorting their tasks by newest, oldest, or due date, deleting a task, and handling errors.

Bootstrap was incorporated in the HTML templates to give the app its front end design, and a “Guest” account was initialized to allow an anonymous user to demo the app without creating an account.
