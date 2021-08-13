from app import create_app, db
from app.blueprints.authentication.models import User



app = create_app()

@app.shell_context_processor
def make_context():
    return {
        'db': db,
        'User': User

    }