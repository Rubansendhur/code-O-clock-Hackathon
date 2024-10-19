from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User Model with login functionality and location
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}>'

    # Method to set password during registration
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check password during login
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Item Model with an image field added for storing file names
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    non_food_category = db.Column(db.String(50), nullable=True)  # Optional for non-food items
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    expiry_date = db.Column(db.String(50), nullable=True)
    story = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True)  # New field for storing image filename or path
    description = db.Column(db.Text, nullable=True)  # New field for AI-generated description
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    allocated_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'<Item {self.name}>'


# ItemRequest Model to track requests made by users
class ItemRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<ItemRequest {self.item_name}>'
