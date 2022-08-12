from app import app,db,migrate,request,redirect,url_for,flash,render_template
from models import Product


@app.route('/admin/product/add',methods=['GET','POST'])
def add_product():
    if request.method=='POST':
        productName=request.form['productName']
        productPrice=request.form['productPrice']
        product=Product(productName=productName,productPrice=productPrice)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('admin_product'))
    return render_template('admin/product/add.html')


@app.route('/admin/product/edit/<int:id>',methods=['GET','POST'])
def edit_product(id):
    product=Product.query.get(id)
    if request.method=='POST':
        product.productName=request.form['productName']
        product.productPrice=request.form['productPrice']
        db.session.commit()
        return redirect(url_for('admin_product'))
    return render_template('admin/product/edit.html',product=product)

@app.route('/admin/product/delete/<int:id>',methods=['GET','POST'])
def delete_product(id):
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin_product'))


@app.route('/admin/product')
def admin_product():
    products=Product.query.all()
    return render_template('admin/product/index.html',products=products)


@app.route('/admin/product/<int:id>')
def product_detail(id):
    product=Product.query.get(id)
    return render_template('admin/product/detail.html',product=product)

