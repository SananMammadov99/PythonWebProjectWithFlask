from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

main = Flask(__name__)

main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(main)
migrate= Migrate(main,db)

from models import *

# import blueprints
from app import *
from admin import *

# register blueprint
main.register_blueprint(public_bp)
main.register_blueprint(admin_bp)


if __name__ == '__main__':
    main.run(debug=True)