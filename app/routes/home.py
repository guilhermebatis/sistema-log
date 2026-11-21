from flask import Blueprint, render_template
from flask_login import login_required
from service.home_layer import get_dashboard_data

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def index():
    data = get_dashboard_data()
    return render_template('home/index.html', data=data)

