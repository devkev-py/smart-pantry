from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from app import *
import os
from pathlib import Path
# from flask import current_app as app
from werkzeug.utils import secure_filename
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

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

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'], salt='mysalt')
        return s.dumps({'user_id': self.user_id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'], salt='mysalt')
        try:
            user_id = s.loads(token)['user_id']
            print(user_id)
        except:
            return None
        return User.query.get(user_id)

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
    memo = db.Column(db.String(100))

    @classmethod
    def create_new(cls, user_id, category_id, food_name, expiration_date, quantity, memo):
        new_food_item = cls(
            user_id=user_id,
            category_id=category_id,
            food_name=food_name,
            purchase_date=datetime.today(),
            expiration_date=expiration_date,
            quantity=quantity,
            memo=memo
        )
        db.session.add(new_food_item)
        db.session.commit()
        return new_food_item
    
    @classmethod
    def delete_with_images(cls, food_id):
        food_item = cls.query.get(food_id)
        if food_item:
            FoodImage.query.filter_by(food_id=food_id).delete()
            db.session.delete(food_item)
            db.session.commit()
            return True
        return False

    @staticmethod
    def fetch_user_inventory(user_id):
        results = db.session.query(
            FoodInventory.food_name,
            FoodInventory.quantity,
            FoodCategory.category_name,
            FoodInventory.expiration_date,
            FoodInventory.memo
        ).join(
            FoodCategory, FoodInventory.category_id == FoodCategory.category_id
        ).filter(
            FoodInventory.user_id == user_id
        ).order_by(
        FoodInventory.expiration_date
        ).all()

        # Calculate status and days to expiry based on expiration date
        for result in results:
            expiry = result.expiration_date
            
            if expiry:
                days_left = (expiry - date.today()).days
                status = "Expired" if days_left <= 0 else f"Good"
                days_left = f"{days_left} days left"
            else:
                days_left = "No Expiry Date"
                status = "Unknown"
            
            yield (result.food_name, result.quantity, result.category_name, days_left, status, result.memo)

    @staticmethod
    def fetch_user_inventory_for_category(user_id, category_id):
        results = db.session.query(
            FoodInventory.food_id,
            FoodInventory.food_name,
            FoodInventory.quantity,
            FoodCategory.category_name,
            FoodInventory.expiration_date,
            FoodInventory.memo,
            FoodImage.image_path
        ).join(
            FoodCategory, FoodInventory.category_id == FoodCategory.category_id
        ).outerjoin(
            FoodImage, FoodInventory.food_id == FoodImage.food_id
        ).filter(
            FoodInventory.user_id == user_id,
            FoodInventory.category_id == category_id
        ).order_by(
            FoodInventory.expiration_date
        ).all()


        # Calculate status and days to expiry based on expiration date
        for result in results:
            expiry = result.expiration_date

            if expiry:
                days_left = (expiry - date.today()).days
                status = "Expired" if days_left <= 0 else f"Good"
                days_left = f"{days_left} days left"
            else:
                days_left = "No Expiry Date"
                status = "Unknown"
            image_path = Path(result.image_path).as_posix() if result.image_path else None
            yield (result.food_name, result.quantity, result.category_name, days_left, status, result.memo, image_path, result.food_id)



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

    @classmethod
    def save_image(cls, food_id, file, upload_folder):
        if file and cls.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_directory = os.path.join(upload_folder, 'food_images')
            if not os.path.exists(image_directory):
                os.makedirs(image_directory)
            image_full_path = os.path.join(image_directory, filename)
            file.save(image_full_path)
            relative_image_path = os.path.join('img','food_images', filename)
            new_food_image = cls(
                food_id=food_id,
                image_path=relative_image_path
            )
            db.session.add(new_food_image)
            db.session.commit()
            return new_food_image
            
    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS