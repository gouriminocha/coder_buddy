from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User
from flask_bcrypt import Bcrypt
import os
import re

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
bcrypt = Bcrypt(app)  # Used indirectly via models
db.init_app(app)

# Simple email validation regex
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration form.
    GET: render registration template.
    POST: validate input, create user, and redirect to success.
    """
    if request.method == 'GET':
        return render_template('register.html')
    # POST handling
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    # Validation
    errors = []
    if not username:
        errors.append('Username is required.')
    if not email:
        errors.append('Email is required.')
    elif not EMAIL_REGEX.match(email):
        errors.append('Invalid email address.')
    if not password:
        errors.append('Password is required.')
    if password != confirm_password:
        errors.append('Passwords do not match.')
    # Uniqueness checks
    if User.query.filter_by(username=username).first():
        errors.append('Username already taken.')
    if User.query.filter_by(email=email).first():
        errors.append('Email already registered.')
    if errors:
        for err in errors:
            flash(err, 'danger')
        return render_template('register.html', username=username, email=email)
    # Create new user (model handles password hashing)
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    flash('Registration successful!', 'success')
    return redirect(url_for('success'))

@app.route('/success')
def success():
    """Render a simple success page after registration."""
    return render_template('success.html')

if __name__ == '__main__':
    # Ensure database tables exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
