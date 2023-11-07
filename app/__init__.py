from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from app.config import *
from flask_mail import Mail, Message
import os
from flask import jsonify


app = Flask(__name__)

#set secret key
app.config['SECRET_KEY'] = '12345'

#DB Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_CONF["username"]}:{DB_CONF["password"]}@{DB_CONF["host"]}/{DB_CONF["dbname"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#MAIL Configurations
app.config['MAIL_SERVER'] = EMAIL_CONF['mailserver']
app.config['MAIL_PORT'] = EMAIL_CONF['mailport']
app.config['MAIL_USERNAME'] = EMAIL_CONF['mailusername']
app.config['MAIL_PASSWORD'] = EMAIL_CONF['mailpassword']
app.config['MAIL_USE_TLS'] = EMAIL_CONF['mailuse_tls']
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

#UPLOAD Configurations
app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'img')

# register blueprints
from app.Blueprints.auth import auth
from app.Blueprints.foodinventory import food_inventory
# from app.routes import main
# app.register_blueprint(main)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(food_inventory, url_prefix='/food-inventory')

from app import routes, models