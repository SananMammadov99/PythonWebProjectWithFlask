from manage import db


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    foods = db.relationship('Food', backref='menu')

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    price = db.Column(db.Float)
    ingredients = db.Column(db.Text)
    image_url = db.Column(db.Text)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
