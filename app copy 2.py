from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import RegistrationForm, LoginForm, ActivityForm, UserProfileForm, SleepMoodForm, BMRForm
import mysql.connector

app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'mysecretkey'

# Configure your MySQL database connection
db_config = {
    "host" : "localhost",
    "user" : "root",
    "password" : "root1234",
    "database" : "hft_fitness"
}

db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
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
            return redirect(url_for('login'))

    return render_template('signup.html', form=form)

def insert_user_data(email, password):
    query = "INSERT INTO users (email, pwd) VALUES (%s, %s)"
    data = (email, password)
    cursor.execute(query, data)
    db_connection.commit()

def validate_email(self, field):
    email = field.data
    # Check if the email already exists in the database
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise ValidationError('Email already exists')  
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Check user credentials in the database
        cursor.execute("SELECT id FROM users WHERE email = %s AND pwd = %s", (email, password))
        user = cursor.fetchall()

        if user:
            session['user_id'] = user[0]  # Store user ID in the session
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'login_failed')

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Use user_id to query the database for user-specific data
        user_id = session['user_id'][0] if 'user_id' in session and isinstance(session['user_id'], tuple) else None 
    
        # Get the total number of activities
        total_activities = get_total_activities(user_id)

        # Get the total calories burned by the user
        total_calories_burned = get_total_calories(user_id)

        # Get the user current mood
        mood_data = fetch_mood_data(user_id)

        # Get the diet plans with total calories
        total_food_calories = calculate_total_food_calories(user_id)
        diet_items = get_user_diet_items(user_id)

        if total_calories_burned is None:
            total_calories_burned = 0

        return render_template('dashboard.html', total_activities=total_activities, total_calories_burned=total_calories_burned, mood_data=mood_data, total_food_calories=total_food_calories, diet_items=diet_items)

    else:
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in

@app.route('/workout')
def workout():
    # Your logic for the workout history page here
    return render_template('workout.html')

@app.route('/diet')
def diet():
    form = BMRForm()

    breakfast_items = fetch_food_items(1)
    lunch_items = fetch_food_items(2)
    dinner_items = fetch_food_items(3) 

    # Retrieve matching_food_items from the session
    matching_food_items = session.pop('matching_food_items', [])   
    
    return render_template('diet.html', form=form, breakfast_items=breakfast_items, lunch_items=lunch_items, dinner_items=dinner_items, matching_food_items=matching_food_items)

@app.route('/add_to_diet_plan', methods=['POST'])
def add_to_diet_plan():
    if request.method == 'POST':

        user_id = session['user_id'][0] if 'user_id' in session and isinstance(session['user_id'], tuple) else None 

        # Get the information about the food item that the user wants to add
        food_name = request.form['food_name']
        calories = request.form['calories']

        insert_query = "INSERT INTO diet_plan (food_name, calories, user_id) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (food_name, calories, user_id))
        db_connection.commit()

    return redirect(request.referrer)

@app.route('/food_search', methods=['POST', 'GET'])
def food_search():
    search_query = request.form.get('foodSearch')  # Get the search query from the form
    if search_query:
        # Query the database to find matching food items
        cursor.execute("SELECT * FROM food WHERE foodName LIKE %s", ('%' + search_query + '%',))
        matching_food_items = cursor.fetchall()
    else:
        matching_food_items = []

    # Store matching_food_items in the session
    session['matching_food_items'] = matching_food_items

    return redirect(url_for('diet'))


def fetch_food_items(category):
    cursor.execute("SELECT foodName, calories, carbohydrates, proteins, fats, descr, imageURL FROM food WHERE categoryID = %s",(category,))
    food_data = cursor.fetchall()
    return food_data 

def calculate_total_food_calories(user_id):
    # Query the diet_plan table to fetch calories for the given user and date
    query = "SELECT SUM(calories) FROM diet_plan WHERE user_id = %s AND DATE(date) = CURRENT_DATE"
    cursor.execute(query, (user_id,))
    total_food_calories = cursor.fetchone()[0]
    return total_food_calories  

def get_user_diet_items(user_id):
    query = "SELECT food_name, calories FROM diet_plan WHERE user_id = %s AND DATE(date) = CURRENT_DATE"
    cursor.execute(query, (user_id,))
    diet_items = cursor.fetchall()
    return diet_items

@app.route('/calculate_bmr', methods=['POST'])
def calculate_bmr():
    form = BMRForm()
    if form.validate_on_submit():
        weight = float(form.weight.data)
        height = float(form.height.data)
        age = int(form.age.data)
        gender = form.gender.data

        # Calculate BMR based on gender (Harris-Benedict equation)
        if gender == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        # Pass the BMR result to the diet.html template
        return render_template('diet.html', form=form, bmr=bmr)
    
    # If the form is not valid, return it to the diet.html template
    return render_template('diet.html', form=form)


@app.route('/drink_water')
def waterTracker():
    return render_template('drink_water.html')

@app.route('/mood_sleep', methods=['GET', 'POST'])
def mood_sleep():
    form = SleepMoodForm()

    # Use user_id to query the database for user-specific data
    user_id = session['user_id'][0] if 'user_id' in session and isinstance(session['user_id'], tuple) else None

    if request.method == 'POST' and form.validate_on_submit():
        sleepiness = form.sleepiness.data
        sleep_hours = form.sleep_hours.data
        mood = form.mood.data

        print(f'Sleepiness: {sleepiness}, Sleep Hours: {sleep_hours}, Mood: {mood}')

        # Insert sleep and mood data into the database
        insert_sleep_data(user_id, sleepiness, sleep_hours)
        insert_mood_data(user_id, mood)

        return redirect(url_for('mood_sleep'))

    sleep_data = fetch_sleep_data(user_id)
    mood_data = fetch_mood_data(user_id)

    total_sleep_duration = sum(entry[3] for entry in sleep_data)

    return render_template('mood_sleep.html', form=form, sleep_data=sleep_data, mood_data=mood_data, total_sleep_duration=total_sleep_duration)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = UserProfileForm()  # Create an instance of the form
    user_profile_data = None  # Initialize user_profile_data as None
    user_id = session['user_id'][0] if 'user_id' in session and isinstance(session['user_id'], tuple) else None

    if request.method == 'POST' and form.validate_on_submit():
        # Access form data using form.data
        name = form.name.data
        email = form.email.data
        gender = form.gender.data
        age = form.age.data
        weight = form.weight.data
        height = form.height.data
        user_id = session.get('user_id')  # Get the user_id from the session

        # Update the user's profile data in the database
        update_user_profile(user_id, name, age, weight, height, gender)  # Implement update_user_profile

        # Redirect back to the profile page to display the updated data
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        user_id = session['user_id'][0] if 'user_id' in session and isinstance(session['user_id'], tuple) else None
        user_profile_data = fetch_user_profile(user_id)  # Implement fetch_user_profile
        form.process(data=user_profile_data)  # Pre-populate the form with existing data

    return render_template('profile.html', form=form, user_profile_data=user_profile_data)


@app.route('/notification')
def notification():
    return render_template('notification.html')
    
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from the session
    return redirect(url_for('login'))

@app.route('/activity', methods=['GET', 'POST'])
def activity():
    form = ActivityForm()
    calories_burned = 0

    user_id = session['user_id'][0] if 'user_id' in session and isinstance(session['user_id'], tuple) else None 

    past_activities = []  # Define an empty list to store past activities

    if form.validate_on_submit():
        activity_type = form.activity_type.data
        duration = form.duration.data
        intensity = form.intensity.data
        calories_burned = calculate_calories(activity_type, duration, intensity)

        if user_id is not None:
            user_id = int(user_id)  # Convert to integer
            insert_activity_data(activity_type, user_id, duration, intensity, calories_burned)
            flash(f'Calories Burned: {calories_burned}', 'success')
        else:
            flash('Error: User ID not found.', 'error')

    # Fetch past activities for the logged-in user
    past_activities = show_activity_data(user_id)
   
    return render_template('activity.html', form=form, calories_burned=calories_burned, past_activities=past_activities)


def calculate_calories(activity_type, duration, intensity):
    if activity_type == "running":
        calories = 7 * duration * intensity
    elif activity_type == "swimming":
        calories = 10 * duration * intensity
    else:
        calories = 5 * duration * intensity
    return calories

def insert_activity_data(activity_type, user_id, duration, intensity, calories_burned):
    query = "INSERT INTO activity (activity_type, user_id, duration, intensity, calories_burned) VALUES (%s, %s, %s, %s, %s)"
    data = (activity_type, user_id, duration, intensity, calories_burned)  # Store data as a tuple

    cursor.execute(query, data)  # Pass data as a single tuple
    db_connection.commit()

def show_activity_data(user_id):
    cursor.execute("SELECT * FROM activity WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    past_activities = cursor.fetchall()
    return past_activities


def get_total_activities(user_id):
    total_activities_today = 0  # Initialize total_activities_today to 0

    cursor.execute("SELECT COUNT(*) FROM activity WHERE user_id = %s AND DATE(created_at) = CURRENT_DATE", (user_id,))
    total_activities_today = cursor.fetchone()[0]
    return total_activities_today


def get_total_calories(user_id):
    cursor.execute("SELECT SUM(calories_burned) FROM activity WHERE user_id = %s AND DATE(created_at) = CURRENT_DATE", (user_id,))
    total_calories_burned = cursor.fetchone()[0]
    return total_calories_burned

def fetch_user_profile(user_id):
    cursor.execute("SELECT name, email, age, weight, height, gender FROM users WHERE id = %s", (user_id,))
    user_profile_data = cursor.fetchone()
    if user_profile_data:
        user_profile = {
            "name": user_profile_data[0],
            "email": user_profile_data[1], 
            "age": user_profile_data[2],
            "weight": user_profile_data[3],
            "height": user_profile_data[4],
            "gender": user_profile_data[5]
        }
        return user_profile
    else:
        return None

def update_user_profile(user_id, name, age, weight, height, gender):
    try:
        user_id = user_id[0] if isinstance(user_id, tuple) else user_id  # Extract the integer user ID
        
        query = "UPDATE users SET name = %s, age = %s, weight = %s, height = %s, gender = %s WHERE id = %s"
        data = (name, age, weight, height, gender, user_id)
        cursor.execute(query, data)
        db_connection.commit()
    except Exception as e:
        print("Error updating user profile:", e)
        db_connection.rollback()  # Roll back the transaction in case of an error

def calculate_sleep_duration(sleepiness, sleep_hours):
    # Define the sleep duration calculation logic based on sleepiness
    if sleepiness == "awake":
        duration = sleep_hours
    elif sleepiness == "tired":
        duration = sleep_hours - 1
    elif sleepiness == "exhausted":
        duration = sleep_hours - 2
    else:
        duration = sleep_hours  # Default to original sleep hours if sleepiness level is not recognized
    
    return max(duration, 0)  # Ensure the duration is non-negative

def insert_sleep_data(user_id, sleepiness, sleep_hours):

    # Calculate sleep duration
    duration = calculate_sleep_duration(sleepiness, sleep_hours)

    query = "INSERT INTO sleep (user_id, sleepiness_level, hours_slept, duration, date) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
    data = (user_id, sleepiness, sleep_hours, duration)

    cursor.execute(query, data)  # Pass data as a single tuple
    db_connection.commit()

def insert_mood_data(user_id, mood):
    query = "INSERT INTO mood (user_id, mood_rating, date) VALUES (%s, %s, CURRENT_TIMESTAMP)"
    data = (user_id, mood)
    cursor.execute(query, data)
    db_connection.commit()

def fetch_sleep_data(user_id):
    cursor.execute("SELECT * FROM sleep WHERE user_id = %s AND DATE(date) = CURRENT_DATE", (user_id,))
    sleep_data = cursor.fetchall()
    return sleep_data

def fetch_mood_data(user_id):
    cursor.execute("SELECT mood_rating, date FROM mood WHERE user_id = %s AND DATE(date) = CURRENT_DATE ORDER BY date DESC LIMIT 1", (user_id,))
    recent_mood_data = cursor.fetchone()
    return recent_mood_data

if __name__ == '__main__':
    app.run(debug=True)

