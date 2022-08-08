from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yummy.db'
db:SQLAlchemy = SQLAlchemy(app)

app.secret_key = 'super secret key'

from routers.menu import menu_blueprint
from routers.menu_item import menu_item_blueprint

app.register_blueprint(menu_blueprint)
app.register_blueprint(menu_item_blueprint)



if __name__ == '__main__':
    app.run(debug=True)
    
    
