from flask import render_template
from app import app
from models import Product

@app.route('/product')
def product():
    products=Product.query.all()
    return render_template('site/product/index.html',products=products)
