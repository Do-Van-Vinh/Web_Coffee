# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from db import MySQL_connect

db = MySQL_connect()
auth = Blueprint('My_auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            #flash('Mật khẩu không khớp.', 'error')
            return render_template('register.html')

        cursor = db.cursor()

        # Kiểm tra người dùng đã tồn tại chưa
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            #flash('Tên đăng nhập đã tồn tại.', 'error')
            return render_template('register.html')

        # Tạo người dùng mới
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, 'customer'))
        db.commit()
        cursor.close()

        #flash('Đăng ký thành công! Bạn có thể đăng nhập.', 'success')
        return redirect(url_for('My_auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #Vị trí trang trả về sau khi login
    next_page = request.args.get('next', '/')

    if request.method == 'POST': #Kiểm tra phương thức truy cập login
        username = request.form['username'] #Tên người dùng đã nhập
        password = request.form['password'] #Mật khẩu đã nhập

        cursor = db.cursor() #Thực hiện truy vấn với CSDL

        # Truy vấn dữ liệu người dùng từ CSDL
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        db.close()
        
        #Kiểm tra dữ liệu đăng nhập
        #Tài khoản tồn tại trong CSDL
        if user:
            session['user'] = user['username']
            session['role'] = user['role']
            #flash('Đăng nhập thành công!', 'success')
            return redirect(next_page)  # Quay lại trang cũ sau khi login
        else:
            return 'Sai tài khoản hoặc mật khẩu!'

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    #flash('Bạn đã đăng xuất!', 'info')
    return redirect(url_for('index'))
