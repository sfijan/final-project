from peewee import *
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '2e351044f7287bd60dfbe2af7e96863c'
database = PostgresqlDatabase('zavrsni', **{'user': 'postgres'})
database.connect()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_view = 'login'


from webapp import routes
