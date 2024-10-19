from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize the Flask app
app = Flask(__name__)

# MySQL configuration using the 'admin' user
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Born%40762004@localhost/digital_waste_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for session management and CSRF protection
app.config['SECRET_KEY'] = 'simple_secret_key_for_hackathon'

# Initialize SQLAlchemy for the database
db = SQLAlchemy(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Initialize Flask-Login for user authentication management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to the login page if the user is not authenticated

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Create an 'uploads' folder in the current working directory

# Set the maximum file size for uploads (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Create the 'uploads' folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Import the User model for user authentication
from app.models import User

# Flask-Login: load user callback function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes after initializing everything
from app import routes
