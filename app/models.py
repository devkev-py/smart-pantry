from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from app import *

class User(db.Model):
    __tablename__ = 'Users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # hashed value
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip_code = db.Column(db.String(255))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class FoodCategory(db.Model):
    __tablename__ = 'FoodCategories'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False)


class FoodInventory(db.Model):
    __tablename__ = 'FoodInventory'
    
    food_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('FoodCategories.category_id'), nullable=False)
    food_name = db.Column(db.String(255), nullable=False)
    purchase_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    quantity = db.Column(db.Integer)
    unit = db.Column(db.String(50))


class SharedFood(db.Model):
    __tablename__ = 'SharedFood'
    
    share_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_id = db.Column(db.Integer, db.ForeignKey('FoodInventory.food_id'), nullable=False)
    sharing_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_for_sharing = db.Column(db.Date)
    status = db.Column(db.Enum('Available', 'Claimed', 'Shared'), nullable=False)


class SharedFoodClaims(db.Model):
    __tablename__ = 'SharedFoodClaims'
    
    claim_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    share_id = db.Column(db.Integer, db.ForeignKey('SharedFood.share_id'), nullable=False)
    claimer_user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    claim_date = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    __tablename__ = 'Notifications'
    
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    notification_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Enum('Read', 'Unread'), nullable=False)


class FoodImage(db.Model):
    __tablename__ = 'FoodImages'
    
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_id = db.Column(db.Integer, db.ForeignKey('FoodInventory.food_id'), nullable=False)
    image_path = db.Column(db.Text, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)