from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from forms import RegistrationForm, LoginForm, ChangePasswordForm
from models import insert_user_data, validate_email
from database import cursor, db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.login'))

    return render_template('./user/signup.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'login_failed')

    return render_template('./user/login.html', form=form)
    

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))
    
@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        email = form.email.data  # Get the user's email

        # Check if the old password matches the user's current password
        cursor.execute("SELECT id FROM users WHERE email = %s AND pwd = %s", (email, old_password))
        user_id = cursor.fetchone()
     
        if user_id:
             # Fetch results to clear the cursor
            cursor.fetchall()

            # Create a new cursor for the update query
            update_cursor = db_connection.cursor()
            update_cursor.execute("UPDATE users SET pwd = %s WHERE id = %s", (new_password, user_id[0]))
            db_connection.commit()
            update_cursor.close()  # Close the update cursor

           
            flash('Password changed successfully.', 'password_changed')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Password change failed. Please check your old password.', 'password_change_failed')

    return render_template('./user/change_password.html', form=form)

# In-memory dictionary to simulate a user database
# users = {
#     'user@example.com': {
#         'name': 'User',
#         'password': 'userpassword'
#     }
# }

# # Generate a unique token (in a real application, use a secure method)
# def generate_reset_token(email):
#     return email

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        if email in users:
            token = generate_reset_token(email)
            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message('Reset Your Password', sender='your_email@example.com', recipients=[email])
            msg.body = f'Click the following link to reset your password: {reset_link}'
            mail.send(msg)
            flash('Password reset link sent to your email.')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid email address.')
    return render_template('./user/forget_password.html')

# Route for resetting password
@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        email = generate_reset_token(request.form['email'])
        if email in users:
            users[email]['password'] = request.form['new_password']
            flash('Password reset successfully. You can now log in with your new password.')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid email address.')
    return render_template('./user/reset_password.html')