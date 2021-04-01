from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import os
from urllib.parse import quote_plus

# server = os.getenv('pikaia.database.windows.net')
# database = os.getenv('pikaia')
# username = os.getenv('pikaia')
# password = os.getenv('Helloadmin123')
# port = os.getenv('PORT', default=1433)
# driver = '{ODBC Driver 17 for SQL Server}'

# connect using parsed URL
# odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+password+';'

odbc_str = "DRIVER={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.0.so.1.1};SERVER=pikaia.database.windows.net;DATABASE=pikaia;UID=pikaia;PWD=Helloadmin123;"
connect_str = 'mssql+pyodbc:///?odbc_connect=' + quote_plus(odbc_str)

# connect with sa url format
# sa_url = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver={driver}"

# SERVER = 'pikaia.database.windows.net'
# DATABASE = 'pikaia'
# DRIVER = 'SQL Server'
# USERNAME = 'pikaia'
# PASSWORD = 'Helloadmin123'
# DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'


# engine = create_engine(DATABASE_CONNECTION)
# connection = engine.connect()

# Configure Database URI:
# params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=pikaia.database.windows.net;DATABASE=pikaia;UID=pikaia;PWD=Helloadmin123;")


# initialization
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = connect_str
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
from pikaia.veiws import views
