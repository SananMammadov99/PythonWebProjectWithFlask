from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

UPLOAD_FOLDER = './yummy_app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yummy.db'
db:SQLAlchemy = SQLAlchemy(app)

app.secret_key = 'super secret key'


from yummy_app import routers