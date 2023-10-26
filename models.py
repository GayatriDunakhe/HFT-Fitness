from database import cursor, db_connection

# authentication
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

# Acticityies
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

# user profile
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

# sleep and mood
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

# diet plans
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