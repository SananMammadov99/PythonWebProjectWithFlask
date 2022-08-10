from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)

UPLOAD_FOLDER = './yummy_app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yummy.db'
db:SQLAlchemy = SQLAlchemy(app)

app.secret_key = 'super secret key'

migrate = Migrate(app, db)



from yummy_app import routers