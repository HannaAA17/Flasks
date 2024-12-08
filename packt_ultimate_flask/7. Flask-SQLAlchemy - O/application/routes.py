from flask import render_template, redirect, url_for, request, session

from application import app
from application.models import Member, Order, Course

@app.route('/')
def index():
    return render_template('home.html')
