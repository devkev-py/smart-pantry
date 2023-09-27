from flask import Blueprint, render_template, flash, redirect, request, url_for,session
from app import app
from app.models import *

# main = Blueprint('main', __name__, template_folder='templates')

@app.route('/')
def index():
    if session.get('logged_in'):
        return render_template('index.html')
    return render_template('auth/login.html')