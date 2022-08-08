from main import app
from flask import request, redirect, url_for, render_template
from main import db
import os
import uuid
from models.menu_item import MenuItem
from models.menu  import Menu

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
    return redirect(url_for('menu_item', menu_id=menu_id))


# update menu item
@app.route('/menu/<int:menu_id>/menu_item/<int:menu_item_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(menu_id, menu_item_id):
    menu_item = MenuItem.query.get_or_404(menu_item_id)
    if request.method == 'POST':
        menu_item.name = request.form['name']
        menu_item.price = request.form['price']
        menu_item.ingredients = request.form['ingredients']
        image = request.files['image']
        if image.filename != '':
            image_url = str(uuid.uuid4()) + '.' + image.filename.split('.')[-1]
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_url))
            menu_item.image = image_url
        db.session.commit()
        return redirect(url_for('menu_item', menu_id=menu_id))
    return render_template('edit_menu_item.html', menu_item=menu_item)\
