from flask import render_template

from app import public_bp

@public_bp.route('/')
def public_index():
    from models import Menu,Food
    menus = Menu.query.all()
    foods = Food.query.all()
    return render_template('index.html',menus=menus,foods=foods)

