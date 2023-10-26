from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from forms import ActivityForm
from models import calculate_calories, insert_activity_data, show_activity_data
from database import cursor, db_connection

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/activity', methods=['GET', 'POST'])
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
   
    return render_template('./activity/activity.html', form=form, calories_burned=calories_burned, past_activities=past_activities)
