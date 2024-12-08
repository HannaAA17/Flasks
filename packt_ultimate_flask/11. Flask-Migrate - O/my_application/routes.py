from flask import Blueprint, render_template

from .models import *


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('home.html')
