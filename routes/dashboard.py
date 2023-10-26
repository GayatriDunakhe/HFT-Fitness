from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from models import get_total_activities, get_total_calories, get_user_diet_items, calculate_total_food_calories, fetch_mood_data

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
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

        return render_template('./dashboard/dashboard.html', total_activities=total_activities, total_calories_burned=total_calories_burned, mood_data=mood_data, total_food_calories=total_food_calories, diet_items=diet_items)

    else:
        return redirect(url_for('auth.login'))  # Redirect to login page if user is not logged in