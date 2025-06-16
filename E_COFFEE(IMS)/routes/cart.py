# routes/shop.py
from flask import Blueprint, request, session, redirect, url_for, render_template
from db import MySQL_connect
from pymysql.cursors import DictCursor

carts = Blueprint('My_cart', __name__)

@carts.route('/cart')
def cart():
    cart = session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total_price=total_price)


@carts.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    db = MySQL_connect()
    with db.cursor(DictCursor) as cursor:
        cursor.execute("SELECT id, name, price, image FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
    db.close()

    if product:
        cart = session.get('cart', {})
        pid = str(product['id'])
        name = product['name']
        price = int(product['price'])
        
        if pid in cart:
            cart[pid]['quantity'] += 1
        else:
            cart[pid] = {
                'name': name,
                'price': price,
                'image': product['image'],
                'quantity': 1
            }


        session['cart'] = cart
        session.modified = True

    return redirect(url_for('My_shop.shop'))  # sửa tên endpoint nếu cần

@carts.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart_quantity(product_id):
    cart = session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        action = request.form.get('action')

        if action == 'increase':
            cart[pid]['quantity'] += 1
        elif action == 'decrease':
            cart[pid]['quantity'] -= 1
            if cart[pid]['quantity'] <= 0:
                del cart[pid]

        session['cart'] = cart
        session.modified = True

    return redirect(url_for('My_cart.cart'))


@carts.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]
        session['cart'] = cart
        session.modified = True

    return redirect(url_for('My_cart.cart'))


