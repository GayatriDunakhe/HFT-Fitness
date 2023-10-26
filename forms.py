from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import  PasswordField, StringField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import DataRequired,EqualTo,Email,Length, Regexp, InputRequired, NumberRange

# this is the Registrationform
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])',
               message='Password must contain at least 8 characters, one uppercase, one lowercase, one special character, and one number.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

# this is Loginform
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# This is activity form
class ActivityForm(FlaskForm):
    activity_type = SelectField('Activity Type', choices=[
        ('running', 'Running'),
        ('swimming', 'Swimming'),
        ('yoga', 'Yoga')
        # Add more activity options here
    ], validators=[InputRequired()])
    duration = IntegerField('Duration (minutes)', validators=[InputRequired()])
    intensity = IntegerField('Intensity', validators=[InputRequired()])
    submit = SubmitField('Calculate Calories')

# This is user profile form
class UserProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=150)])
    weight = DecimalField('Weight', validators=[NumberRange(min=0, max=1500)])
    height = DecimalField('Height', validators=[NumberRange(min=0, max=300)])

# This is for sleep and mood
class SleepMoodForm(FlaskForm):
    sleep_hours = IntegerField('Sleep Hours')
    mood = SelectField('Mood', choices=[
        ('Happy😃', 'Happy😃'),
        ('Sad☹️', 'Sad☹️'),
        ('Angry😡', 'Angry😡'),
        ('Calm😌', 'Calm😌')
    ])
    sleepiness = SelectField('Sleepiness', choices=[
        ('awake', 'Awake😵'),
        ('tired', 'Tired🥴'),
        ('exhausted', 'Exhausted😑')
    ])
    submit = SubmitField('Submit')

class BMRForm(FlaskForm):
    weight = StringField('Weight (kg):', validators=[InputRequired()])
    height = StringField('Height (cm):', validators=[InputRequired()])
    age = StringField('Age (years):', validators=[InputRequired()])
    gender = SelectField('Gender:', choices=[('male', 'Male'), ('female', 'Female')])
    submit = SubmitField('Calculate BMR')
