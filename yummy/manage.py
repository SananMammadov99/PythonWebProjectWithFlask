from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import send_from_directory


main = Flask(__name__)

main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

main.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(main)
migrate= Migrate(main,db)

main.config['SECRET_KEY'] = 'secret-key'

from models import *

@main.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(main.config['UPLOAD_FOLDER'], filename)  


# import blueprints
from app import *
from admin import *

# register blueprint
main.register_blueprint(public_bp)
main.register_blueprint(admin_bp)


if __name__ == '__main__':
    main.run(debug=True)