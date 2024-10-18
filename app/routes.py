import random
from flask import Request, render_template, request, redirect, url_for
from app import app, db
from app.models import Item, ItemRequest
from geopy.distance import geodesic
from flask_login import login_required


# Route for displaying all items
@app.route('/')
def index():
    items = Item.query.all()  # Fetch all items from the database
    return render_template('index.html', items=items)

@app.route('/list-item', methods=['GET', 'POST'])
@login_required
def list_item():
    if request.method == 'POST':
        name = request.form['name']
        item_category = request.form['category']
        non_food_category = request.form.get('non_food_category') if item_category == 'Non-Food' else None
        quantity = request.form['quantity']
        location = request.form['location']
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        expiry_date = request.form.get('expiry_date') if item_category == 'Food' else None
        story = request.form.get('story')

        # Create and add a new item to the database
        new_item = Item(
            name=name,
            type=item_category if item_category == 'Food' else non_food_category,
            quantity=quantity,
            location=location,
            latitude=latitude,
            longitude=longitude,
            expiry_date=expiry_date,
            story=story,
            user_id=current_user.id
        )
        db.session.add(new_item)

        # Award points for listing the item
        current_user.points += 10
        db.session.commit()

        flash('Item listed successfully! You earned 10 points!', 'success')
        return redirect(url_for('index'))

    return render_template('list_item.html')


# Route for matching items by location and type
@app.route('/match-items', methods=['GET', 'POST'])
@login_required  # Ensure only logged-in users can access
def match_items():
    if request.method == 'POST':
        item_type = request.form['item_type']
        user_location = (float(current_user.location.split(',')[0]), float(current_user.location.split(',')[1]))  # User's saved location

        items = Item.query.filter_by(type=item_type).all()
        matched_items = []

        # Match items based on proximity (e.g., 20 km radius)
        for item in items:
            item_location = (float(item.location.split(',')[0]), float(item.location.split(',')[1]))  # Assuming item locations are saved as lat/lon
            distance = geodesic(user_location, item_location).km
            if distance <= 20:
                matched_items.append(item)

        return render_template('matched_items.html', matched_items=matched_items)

    return render_template('match_form.html')

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User, Item
from app.forms import RegistrationForm, LoginForm

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, location=form.location.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect if already logged in
    
    form = LoginForm()
    
    if form.validate_on_submit():
        print("Form submitted")  # Check if form is submitting
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            print(f"User found: {user.username}")  # Check if user exists
        else:
            print("User not found")
        
        if user and user.check_password(form.password.data):
            print("Password correct")
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        
        else:
            print("Invalid username or password")
            flash('Invalid username or password. Please try again.', 'danger')
    
    return render_template('login.html', form=form)


# Logout Route
@app.route('/logout')
@login_required  # Ensure only logged-in users can log out
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/search_items', methods=['GET'])
def search_items():
    query = request.args.get('query')

    # Filter items from the database based on the search query
    if query:
        matched_items = Item.query.filter(Item.name.ilike(f'%{query}%')).all()  # Get matched items
    else:
        matched_items = []

    # Get all items to render on the page
    all_items = Item.query.all()

    # Pass the matched items and search query to the template
    return render_template('index.html', items=all_items, matched_items=matched_items, search_query=query)



@app.route('/request_item/<int:item_id>', methods=['GET'])
@login_required
def request_item(item_id):
    item = Item.query.get(item_id)
    
    # Check if the item is already allocated
    if item.allocated_to:
        flash('Item already requested by another user.', 'danger')
        return redirect(url_for('index'))
    
    # Allocate the item to the current user
    item.allocated_to = current_user.id
    current_user.points += 5  # Add points for requesting an item
    db.session.commit()
    
    flash('Item successfully requested! You earned 5 points!', 'success')
    return redirect(url_for('index'))


# Dashboard Route (Flask)
@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch user's listed items
    user_items = Item.query.filter_by(user_id=current_user.id).all()

    # Fetch user's requested items
    requested_items = ItemRequest.query.filter_by(user_id=current_user.id).all()

    # Fetch total points for the current user
    user_points = current_user.points

    # Set the current level and progress
    next_milestone = 100  # For example, each level is achieved every 100 points
    points_percentage = min((user_points / next_milestone) * 100, 100)
    
    # Set current level based on points (e.g., level increases every 100 points)
    level = user_points // next_milestone + 1

    # Random surprise gifts for reaching 100%
    if points_percentage == 100:
        gifts = ['Extra 20 points', 'Free Merchandise', 'Digital Certificate']
        surprise_gift = random.choice(gifts)
    else:
        surprise_gift = None

    return render_template(
        'dashboard.html',
        user_items=user_items,
        requested_items=requested_items,
        points=user_points,
        points_percentage=points_percentage,
        level=level,
        surprise_gift=surprise_gift
    )


@app.route('/leaderboard')
@login_required
def leaderboard():
    # Query top 10 users by points
    top_users = User.query.order_by(User.points.desc()).limit(10).all()
    return render_template('leaderboard.html', top_users=top_users)





