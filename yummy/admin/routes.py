from hashlib import new
from admin import admin_bp
from flask import render_template,request,redirect,url_for,flash
from admin.forms import *
from werkzeug.utils import secure_filename



@admin_bp.route('/menu/add',methods=['GET','POST'])
def admin_add_menu():
    form = MenuForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            from models import Menu,db
            menu = Menu(name=form.name.data)
            db.session.add(menu)
            db.session.commit()
            # redirect to all menus
            return redirect(url_for('admin.admin_menu'))

    return render_template('/menu/add.html', title='Add new menu', form=form)

# get all menus
@admin_bp.route('/menu')
def admin_menu():
    from models import Menu
    form= MenuForm()
    menus = Menu.query.all()
    return render_template('menu/menu.html',menus=menus,form=form)

# delete menu
@admin_bp.route('/menu/<int:id>/delete')
def admin_delete_menu(id):
    from models import Menu,db
    menu = Menu.query.get(id)
    db.session.delete(menu)
    db.session.commit()
    return redirect(url_for('admin.admin_menu'))

# edit menu
@admin_bp.route('/menu/<int:id>/edit',methods=['GET','POST'])
def admin_edit_menu(id):
    from models import Menu,db
    menu = Menu.query.get(id)
    form = MenuForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            menu.name = form.name.data
            db.session.commit()
            return redirect(url_for('admin.admin_menu'))
    form.name.data = menu.name
    form.submit.label.text = 'Update'
    return render_template('menu/edit.html',title='Edit menu',form=form)



# create food based food model
@admin_bp.route('/menu/<int:id>/food/add',methods=['GET','POST'])
def admin_add_food(id):
    from models import Menu,Food,db
    menu = Menu.query.get(id)
    form = FoodForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            from manage import main
            import os
            import uuid

            # upload image
            image_file = request.files['image_url']
            filename = secure_filename(image_file.filename)
            # generate random name for image
            random_name = str(uuid.uuid4())
            new_name= random_name + filename

            image_file.save(os.path.join(main.config['UPLOAD_FOLDER'],new_name))       

            food = Food(title=form.name.data,price=form.price.data,ingredients=form.ingredients.data,image_url=new_name,menu_id=menu.id)
            db.session.add(food)
            db.session.commit()
            return redirect(url_for('admin.admin_food', id=menu.id))
    return render_template('menu/add_food.html',title='Add food',form=form,menu=menu)



# all food items
@admin_bp.route('/menu/<int:id>/food')
def admin_food(id):
    from models import Menu,Food
    menu = Menu.query.get(id)
    foods = Food.query.filter_by(menu_id=id)
    return render_template('menu/food.html',foods=foods,menu=menu)

# delete food item
@admin_bp.route('/menu/<int:id>/food/<int:food_id>/delete')
def admin_delete_food(id,food_id):
    from models import Food,db
    food = Food.query.get(food_id)
    db.session.delete(food)
    db.session.commit()
    return redirect(url_for('admin.admin_food',id=id))

# edit food
@admin_bp.route('/menu/<int:id>/food/<int:food_id>/edit',methods=['GET','POST'])
def admin_edit_food(id,food_id):
    from models import Food,db
    food = Food.query.get(food_id)
    form = FoodForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            food.title = form.name.data
            food.price = form.price.data
            food.ingredients = form.ingredients.data
            db.session.commit()
            return redirect(url_for('admin.admin_food',id=id))
    form.name.data = food.title
    form.price.data = food.price
    form.ingredients.data = food.ingredients
    form.submit.label.text = 'Update'
    return render_template('menu/edit_food.html',title='Edit food',form=form,menu=food.menu,food=food)


@admin_bp.route('/')
def admin_index():
    return render_template('/dashboard.html', title='Admin')