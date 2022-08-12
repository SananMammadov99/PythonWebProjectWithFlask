from app import db

#generate class with productName and productPrice   
class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    productName=db.Column(db.String(100),nullable=True)
    productPrice=db.Column(db.Integer,nullable=True)
    is_active=db.Column(db.Boolean,default=True)
    add_date=db.Column(db.DateTime)
    
class Orders(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    order_date=db.Column(db.DateTime)
    order_status=db.Column(db.String(100),nullable=True)
    order_total=db.Column(db.Integer,nullable=True)
    is_active=db.Column(db.Boolean,default=True)
    add_date=db.Column(db.DateTime)