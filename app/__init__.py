from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
csrf = CSRFProtect()
admin = Admin(name='MyApp Admin', template_mode='bootstrap4')

# Ensure login manager knows where to redirect for login
login.login_view = 'auth.login'

class AdminModelView(ModelView):
    def is_accessible(self):
        # Only allow access if the user is authenticated and has an 'is_admin' attribute set to True
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # Redirect users who don't have access to the login page
        return redirect(url_for('auth.login', next=request.url))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize app with extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    csrf.init_app(app)
    admin.init_app(app)
    
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
    
    # Add administrative views here
    from app.models import User, Role
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Role, db.session))

    return app