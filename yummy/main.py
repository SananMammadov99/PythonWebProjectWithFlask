from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yummy.db'
db:SQLAlchemy = SQLAlchemy(app)

app.secret_key = 'super secret key'


from routers import menu
from routers import menu_item



if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='