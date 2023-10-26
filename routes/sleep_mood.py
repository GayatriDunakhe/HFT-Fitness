from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from forms import SleepMoodForm
from models import insert_sleep_data, insert_mood_data, fetch_sleep_data, fetch_mood_data
from database import cursor, db_connection

sleep_mood_bp = Blueprint('sleep_mood', __name__)

@sleep_mood_bp.route('/mood_sleep', methods=['GET', 'POST'])
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

        return redirect(url_for('sleep_mood.mood_sleep'))

    sleep_data = fetch_sleep_data(user_id)
    mood_data = fetch_mood_data(user_id)

    total_sleep_duration = sum(entry[3] for entry in sleep_data)

    return render_template('./sleep_mood/mood_sleep.html', form=form, sleep_data=sleep_data, mood_data=mood_data, total_sleep_duration=total_sleep_duration)
