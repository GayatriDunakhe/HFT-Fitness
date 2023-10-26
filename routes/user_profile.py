from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from forms import UserProfileForm
from models import update_user_profile, fetch_user_profile
from database import cursor, db_connection

user_profile_bp = Blueprint('user_profile', __name__)

@user_profile_bp.route('/profile', methods=['GET', 'POST'])
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
        return redirect(url_for('user_profile.profile'))

    elif request.method == 'GET':
        user_id = session['user_id'][0] if 'user_id' in session and isinstance(session['user_id'], tuple) else None
        user_profile_data = fetch_user_profile(user_id)  # Implement fetch_user_profile
        form.process(data=user_profile_data)  # Pre-populate the form with existing data

    return render_template('./user/profile.html', form=form, user_profile_data=user_profile_data)

