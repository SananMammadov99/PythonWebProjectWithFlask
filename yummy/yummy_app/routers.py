from yummy_app import app,db
from yummy_app.models import Menu, MenuItem, User

from flask import request,redirect,url_for,render_template, session
import os, uuid

# Burda yummy_app yazamasam basa dusmur helper modulunu. Onu tam anlamadim
import yummy_app.helper as h

# create menu item
@app.route('/menu/<int:menu_id>/menu_item/new', methods=['GET', 'POST'])
@h.login_required
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
@h.login_required
def menu_item(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    menu_items = MenuItem.query.filter_by(menu_id=menu_id).all()
    return render_template('menu_item.html', menu=menu, menu_items=menu_items)


@app.route('/menu/<int:menu_id>/menu_item/<int:menu_item_id>/delete', methods=['GET'])  
@h.login_required
def delete_menu_item(menu_id, menu_item_id):
    menu_item = MenuItem.query.get_or_404(menu_item_id)
    db.session.delete(menu_item)
    db.session.commit()
    return redirect(url_for('menu_item', menu_id=menu_id))


# update menu item
@app.route('/menu/<int:menu_id>/menu_item/<int:menu_item_id>/edit', methods=['GET', 'POST'])
@h.login_required
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

@app.route('/menu', methods=['GET', 'POST'])
@h.login_required
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
@h.login_required
def delete_menu(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    db.session.delete(menu)
    db.session.commit()
    return redirect(url_for('menu'))

# edit menu
@app.route('/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
@h.login_required
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


# register user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and not h.is_logged_in() :
        
        username = request.form['username']
        password = request.form['password']

        # check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html', error='User already exists')
            
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        # set session for user
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('register.html')

# login user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and not h.is_logged_in():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and user.password == password:
            # set session for user
            session['username'] = username
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    return render_template('login.html')


# check if user admin true
@app.route('/admin', methods=['GET'])
@h.login_required
def admin():
    if h.is_admin():
        return 'you are admin'
    return 'you are not admin'

# logout user
@app.route('/logout', methods=['GET'])
@h.login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

