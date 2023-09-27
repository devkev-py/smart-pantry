from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from app.config import DB_CONF

app = Flask(__name__)

#set secret key
app.config['SECRET_KEY'] = '12345'

#DB Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_CONF["username"]}:{DB_CONF["password"]}@{DB_CONF["host"]}/{DB_CONF["dbname"]}'
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# register blueprints
from app.Blueprints.auth import auth
# from app.routes import main
# app.register_blueprint(main)
app.register_blueprint(auth, url_prefix='/auth')

from app import routes, models