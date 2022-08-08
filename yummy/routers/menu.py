from flask import request, redirect, url_for, render_template, Blueprint
from main import db
from models.menu import Menu
from models.menu_item import MenuItem


menu_blueprint = Blueprint('menu_blueprint', __name__)
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        name = request.form['name']
        menu = Menu(name=name)
        db.session.add(menu)
        db.session.commit()
        return redirect(url_for('menu'))
    menus = Menu.query.all()
    return render_template('menu.html', menus=menus)


# delete menu
@app.route('/menu/<int:menu_id>/delete', methods=['GET'])
def delete_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    db.session.delete(menu)
    db.session.commit()
    return redirect(url_for('menu'))

    # edit menu
@app.route('/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    if request.method == 'POST':
        menu.name = request.form['name']
        db.session.commit()
        return redirect(url_for('menu'))
    return render_template('edit_menu.html', menu=menu)
    


@app.route('/')
def index():
    menus = Menu.query.all()
    menu_items = MenuItem.query.all()
    return render_template('index.html', menus=menus, menu_items=menu_items)

