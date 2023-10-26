from flask import Blueprint, render_template

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/notification')
def notification():
    return render_template('notification.html')
 
    
