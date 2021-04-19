import pyodbc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

# Using pyodbc driver to connect to the cloud database
drivers = [item for item in pyodbc.drivers()]
driver = drivers[-1]

"+driver+"

odbc_str = "DRIVER={" + driver + "};SERVER=pikaia.database.windows.net;DATABASE=pikaia;UID=pikaia;PWD=Helloadmin123;"
connect_str = 'mssql+pyodbc:///?odbc_connect=' + quote_plus(odbc_str)

# initialization
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = connect_str
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
db.init_app(app)

# Local Database

# app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pikaia.db'
# app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
# db = SQLAlchemy(app)

from pikaia.admin import routes
from pikaia.emotion import routes
from pikaia.chatbot import routes
from pikaia.music_recommender import routes
from pikaia.user import routes
from pikaia.quotes import routes
from pikaia.veiws import views
from pikaia.binaural import routes
