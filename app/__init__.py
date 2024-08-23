from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize app with extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    csrf.init_app(app)
    
    # Set up the user loader
    from app.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from app.routes import main_bp
    from app.auth.routes import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app