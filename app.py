from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)
app.static_folder = 'static'

db_config = {
    "host" : "localhost",
    "user" : "root",
    "password" : "root1234",
    "database" : "hft_fitness"
}

db_connection = mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/exercise')
def exercise():
    return render_template('exercise.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)