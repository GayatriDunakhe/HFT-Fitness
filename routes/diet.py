from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from forms import BMRForm
from models import fetch_food_items
from database import cursor, db_connection

diet_bp = Blueprint('diet', __name__)

@diet_bp.route('/diet')
def diet():
    form = BMRForm()

    breakfast_items = fetch_food_items(1)
    lunch_items = fetch_food_items(2)
    dinner_items = fetch_food_items(3) 

    # Retrieve matching_food_items from the session
    matching_food_items = session.pop('matching_food_items', [])   
    
    return render_template('./diet/diet.html', form=form, breakfast_items=breakfast_items, lunch_items=lunch_items, dinner_items=dinner_items, matching_food_items=matching_food_items)

@diet_bp.route('/add_to_diet_plan', methods=['POST'])
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

@diet_bp.route('/food_search', methods=['POST', 'GET'])
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

    return redirect(url_for('diet.diet'))

@diet_bp.route('/calculate_bmr', methods=['POST'])
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
        return render_template('./diet/diet.html', form=form, bmr=bmr)
    
    # If the form is not valid, return it to the diet.html template
    return render_template('./diet/diet.html', form=form)


@diet_bp.route('/drink_water')
def waterTracker():
    return render_template('./diet/drink_water.html')