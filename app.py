# app.py
from flask import Flask, render_template
from forms import RegistrationForm, LoginForm
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.diet import diet_bp
from routes.user_profile import user_profile_bp
from routes.sleep_mood import sleep_mood_bp
from routes.activity import activity_bp
from routes.notification import notification_bp
# from flask_mail import Mail, Message

app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'mysecretkey'

# Configure Flask-Mail
# app.config['MAIL_SERVER'] = 'your_mail_server'
# app.config['MAIL_PORT'] = 587  # Port for your mail server
# app.config['MAIL_USERNAME'] = 'your_email@example.com'
# app.config['MAIL_PASSWORD'] = 'your_email_password'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False

# # Initialize Flask-Mail
# mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(diet_bp)
app.register_blueprint(user_profile_bp)
app.register_blueprint(sleep_mood_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(notification_bp)

if __name__ == '__main__':
    app.run(debug=True)
