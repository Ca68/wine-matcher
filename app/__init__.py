from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'authentication.login'
    login_manager.login_message = 'You do not have access to this page. Please log in to continue'
    login_manager.login_message_category = 'danger'

    moment.init_app(app)
    

    from app.blueprints.authentication import bp as authentication
    app.register_blueprint(authentication)


# building the rest of the flask application
    with app.app_context():

        from app.blueprints.main import bp as main
        app.register_blueprint(main)


        

    return app
