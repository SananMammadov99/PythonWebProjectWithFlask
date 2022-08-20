from flask import render_template

from app import public_bp

@public_bp.route('/')
def public_index():
    return render_template('index.html')
