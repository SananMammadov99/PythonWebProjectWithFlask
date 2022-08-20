from flask import Blueprint


public_bp = Blueprint('public', __name__, template_folder='templates',static_folder='static', static_url_path='/app/static')

from app.routers import *
from app import public_bp