from yummy_app import db


# create menu item with ingredients and image
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(8), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id', ondelete='CASCADE'), nullable=True)
    menu = db.relationship('Menu', backref=db.backref('menu_items', lazy=True))
    ingredients = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(250), nullable=False)


# Create a category table
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    menu_item = db.relationship('MenuItem', backref='menus', lazy=True)

# user model
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    password=db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"User('{self.username}')"

# db.create_all()