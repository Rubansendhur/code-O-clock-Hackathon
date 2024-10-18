from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User Model with login functionality and location
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0)

    # Method to set password during registration
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check password during login
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Item Model remains the same
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    non_food_category = db.Column(db.String(50), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    expiry_date = db.Column(db.String(50), nullable=True)
    story = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    allocated_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

