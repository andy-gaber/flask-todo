from app import app, db
from app.models import User, Task

# 'flask shell' in terminal to use python shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task}
