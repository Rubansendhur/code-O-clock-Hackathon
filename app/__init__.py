from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)



# MySQL configuration using the 'admin' user
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ruban:0000@localhost/digital_waste_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Simple hardcoded secret key for CSRF protection
app.config['SECRET_KEY'] = 'simple_secret_key_for_hackathon'

db = SQLAlchemy(app)

# Add this to your existing code in __init__.py
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if user is not authenticated

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes
