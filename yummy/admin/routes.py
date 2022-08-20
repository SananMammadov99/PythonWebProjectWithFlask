from turtle import title
from admin import admin_bp
from flask import render_template,request
from models import *


@admin_bp.route('/menu/add')
def admin_add_menu():
    return render_template('/menu/add.html', title='Add new menu')


@admin_bp.route('/')
def admin_index():
    return 'Admin index'