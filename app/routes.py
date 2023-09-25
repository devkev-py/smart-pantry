from flask import render_template, flash, redirect, request, url_for
from app import app
from app.models import *


@app.route('/')
def test_db():
    user = User.query.first()
    return str(user)  # returning the string representation of the user
