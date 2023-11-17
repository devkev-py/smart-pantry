from flask import Blueprint, render_template, request, redirect, url_for, Response, flash,session
from app.models import *

your_shared_food = Blueprint('yourSharedFood', __name__, template_folder='templates')

@your_shared_food.route('/')
def index():
    if session.get('logged_in'):
        user_id = session['user_id']
        shared_items = SharedFood.get_user_shared_items(user_id)
        shared_items_list = [
            {'share_id': item[0], 'title': item[1], 'description': item[2], 'quantity': item[3], 'food_name': item[4], 'expiration_date': item[5]}
            for item in shared_items
        ]
        return render_template('your-shared-food.html', shared_items=shared_items_list)
    return render_template('auth/login.html')

@your_shared_food.route('/dashboard')
def dashboard():
    pass

@your_shared_food.route('/share-food', methods=['GET', 'POST'])
def share_food():
    if request.method == 'POST':
        food_id = request.form.get('food_id')
        post_title = request.form.get('post_title')
        description = request.form.get('description')
        status = 'Shared'
        quantity_to_share = int(request.form.get('quantity'))
        available_quantity = int(request.form.get('available_quantity'))
        quantity_being_shared = SharedFood.get_total_quantity_being_shared(food_id)
        expiry_date = FoodInventory.query.filter(FoodInventory.food_id == food_id).first().expiration_date

        # Adjust quantity
        quantity_to_share = quantity_to_share if quantity_being_shared + quantity_to_share <= available_quantity else available_quantity - quantity_being_shared
        # check if food has expired
        if expiry_date and expiry_date[0] < date.today():
            flash('You cannot share an expired food item')
            return redirect(url_for('foodinventory.dashboard'))

        if quantity_to_share <= 0:
            flash('You have already shared all the available quantity for this food item')
            return redirect(url_for('foodinventory.dashboard'))

        new_shared_food = SharedFood.create_new(
            food_id=food_id,
            status=status,
            title=post_title,
            description=description,
            quantity=quantity_to_share
        )
        return redirect(url_for('foodinventory.dashboard'))