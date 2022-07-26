from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy
import os
import uuid


app = Flask(__name__)

UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yummy.db'
db = SQLAlchemy(app)

app.secret_key = 'super secret key'


# Create a category table
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    menu_item = db.relationship('MenuItem', backref='menus', lazy=True)


# create menu item with ingredients and image
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(8), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id', ondelete='CASCADE'), nullable=True)
    menu = db.relationship('Menu', backref=db.backref('menu_items', lazy=True))
    ingredients = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(250), nullable=False)



@app.route('/')
def index():
    menus = Menu.query.all()
    menu_items = MenuItem.query.all()
    return render_template('index.html', menus=menus, menu_items=menu_items)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        name = request.form['name']
        menu = Menu(name=name)
        db.session.add(menu)
        db.session.commit()
        flash('New menu item was successfully created')
        return redirect(url_for('menu'))
    menus = Menu.query.all()
    return render_template('menu.html', menus=menus)


# delete menu
@app.route('/menu/<int:menu_id>/delete', methods=['GET'])
def delete_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    db.session.delete(menu)
    db.session.commit()
    flash('Menu item was successfully deleted')
    return redirect(url_for('menu'))

# create menu item
@app.route('/menu/<int:menu_id>/menu_item/new', methods=['GET', 'POST'])
def new_menu_item(menu_id):
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        ingredients = request.form['ingredients']
        image = request.files['image']

        image_url = str(uuid.uuid4()) + '.' + image.filename.split('.')[-1]
        if image.filename != '':
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_url))
        else:
            image_url = 'image.jpg'
            
        menu = Menu.query.get_or_404(menu_id)
        menu_item = MenuItem(name=name, price=price, ingredients=ingredients, image=image_url, menu=menu)
        db.session.add(menu_item)
        db.session.commit()
        flash('New menu item was successfully created')
        return redirect(url_for('menu'))
    menu = Menu.query.get_or_404(menu_id)
    return render_template('new_menu_item.html', menu=menu)


@app.route('/menu/<int:menu_id>/menu_item', methods=['GET'])
def menu_item(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    menu_items = MenuItem.query.filter_by(menu_id=menu_id).all()
    return render_template('menu_item.html', menu=menu, menu_items=menu_items)


@app.route('/menu/<int:menu_id>/menu_item/<int:menu_item_id>/delete', methods=['GET'])  
def delete_menu_item(menu_id, menu_item_id):
    menu_item = MenuItem.query.get_or_404(menu_item_id)
    db.session.delete(menu_item)
    db.session.commit()
    flash('Menu item was successfully deleted')
    return redirect(url_for('menu_item', menu_id=menu_id))
    
# get all

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='