from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from config import DB_CONF

app = Flask(__name__)


#DB Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_CONF["username"]}:{DB_CONF["password"]}@{DB_CONF["host"]}/{DB_CONF["dbname"]}'
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import routes, models