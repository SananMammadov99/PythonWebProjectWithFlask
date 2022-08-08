from main import db

# Create a category table
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    menu_item = db.relationship('MenuItem', backref='menus', lazy=True)
