# routes/__init__.py
#from flask import Blueprint

def all_routes(app): #Các chức năng của app
    from .auth import auth
    from .shop import products
    from .cart import carts
    app.register_blueprint(auth)#Sử dụng hàm register_blueprint của flask
    app.register_blueprint(products)
    app.register_blueprint(carts)