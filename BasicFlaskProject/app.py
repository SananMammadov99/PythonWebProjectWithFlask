from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db=SQLAlchemy(app)
migrate=Migrate(app,db)



if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)