#hg
# routes/shop.py
from flask import Blueprint, request, session, redirect, url_for, render_template
from functools import wraps
from db import MySQL_connect
from pymysql.cursors import DictCursor
from werkzeug.utils import secure_filename
import os

products = Blueprint('My_shop', __name__)

#
@products.route('/shop')
def shop():
    user_role = session.get('role', 'customer')
    
    db = MySQL_connect()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM product_category") #Truy vấn dữ liệu từ danh mục sản phẩm
        categories = cursor.fetchall()
        
        category_id = request.args.get('category')
        keyword = request.args.get('search')

        if category_id:
            cursor.execute("SELECT * FROM products WHERE category_id = %s", (category_id,))
        elif keyword:
            cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + keyword + '%',))
        else:    
            cursor.execute("SELECT * FROM products")  #Truy vấn tất cả các danh mục của bảng
        products = cursor.fetchall()
    db.close()
    
    return render_template('shop.html', products=products, role=user_role, categories=categories)

#
@products.route('/product/<int:product_id>')
def product_detail(product_id):
    db = MySQL_connect()
    with db.cursor(DictCursor) as cursor:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
    db.close()

    if not product:
        return "Sản phẩm không tồn tại", 404

    return render_template('product_detail.html', product=product)


# ---- Gộp decorator vào đây luôn ----
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return "Bạn không có quyền truy cập trang này.", 403
        return f(*args, **kwargs)
    return decorated_function

# ---- Route thêm sản phẩm ----
@products.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    db = MySQL_connect()
    with db.cursor(DictCursor) as cursor:
        cursor.execute("SELECT * FROM product_category")
        categories = cursor.fetchall()
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category_id = request.form['category_id']
        description = request.form['description']
        image = request.files['image']
        filename = secure_filename(image.filename)
        image_path = os.path.join('static/img_product', filename)
        image.save(image_path)
        
        db = MySQL_connect()
        with db.cursor() as cursor:
            cursor.execute("INSERT INTO products (name, price, category_id, description, image)VALUES (%s, %s, %s, %s, %s)", (name, price, category_id, description, filename))
            db.commit()
        db.close()
        return redirect(url_for('My_shop.shop'))

    return render_template('products.html', action='Thêm', product=None, categories = categories)

# ---- Route sửa sản phẩm ----
@products.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    db = MySQL_connect()
    with db.cursor(DictCursor) as cursor:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            return "Sản phẩm không tồn tại", 404

        if request.method == 'POST':
            name = request.form['name']
            price = request.form['price']
            category_id = request.form['category_id']
            description = request.form['description']
            image = request.files['image']
            cursor.execute("UPDATE products SET name = %s, price = %s, category_id = %s, description = %s, image = %s WHERE id = %s", (name, price, category_id, description, image, product_id))
            db.commit()
            db.close()
            return redirect(url_for('My_shop.shop'))

    db.close()
    return render_template('products.html', action='Sửa', product=product)

# ---- Route xoá sản phẩm ----
@products.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    db = MySQL_connect()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        db.commit()
    db.close()
    return redirect(url_for('My_shop.shop'))