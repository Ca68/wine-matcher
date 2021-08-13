from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200))
    image = db.Column(db.String)
    bio = db.Column(db.Text)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def create_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User: {self.email}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)