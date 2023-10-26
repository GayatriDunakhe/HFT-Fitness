from flask import Blueprint, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
import mysql.connector

user_routes = Blueprint('user', __name__)

# Configure your MySQL database connection
db_config = {
    "host" : "localhost",
    "user" : "root",
    "password" : "root1234",
    "database" : "hft_fitness"
}

db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

@user_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            flash('Password and confirm password do not match.', 'password_mismatch')
        else:
            insert_user_data(email, password)

            flash('Registration successful. You can now log in.', 'registration_success')
            return redirect(url_for('user.login'))

    return render_template('signup.html', form=form)

def insert_user_data(email, password):
    query = "INSERT INTO users (email, pwd) VALUES (%s, %s)"
    data = (email, password)
    cursor.execute(query, data)
    db_connection.commit()
    db_connection.close()

def validate_email(self, field):
    email = field.data
    # Check if the email already exists in the database
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise ValidationError('Email already exists')  
    # Close the result set after fetching results
    cursor.close() 

@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Check user credentials in the database
        cursor.execute("SELECT * FROM users WHERE email = %s AND pwd = %s", (email, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('user.dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'login_failed')

    return render_template('login.html', form=form)

@user_routes.route('/profile')
def profile():
    return render_template('profile.html')

@user_routes.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')