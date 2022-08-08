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
