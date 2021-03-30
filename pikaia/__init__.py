from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import urllib.parse 

# Configure Database URI: 
params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=pikaia.database.windows.net;DATABASE=pikaia;UID=pikaia;PWD=Helloadmin123;")

#
# initialization
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)

# # # Local Database
# app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pikaia.db'
# app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
# db = SQLAlchemy(app)

from pikaia.admin import routes
from pikaia.chatbot import routes
from pikaia.music_recommender import routes
from pikaia.user import routes
from pikaia.quotes import routes
