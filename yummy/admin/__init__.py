from flask import Blueprint

admin_bp = Blueprint('admin',__name__,template_folder='templates',url_prefix='/admin',static_folder='static',static_url_path='/admin/static')

from admin.routes import *
from admin import admin_bp