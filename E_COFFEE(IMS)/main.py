#main.py
from flask import Flask, render_template
from db import MySQL_connect
from routes import all_routes

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key_demo"  # Cần thiết cho đăng nhập

#db = MySQL_connect()

all_routes(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/gioi_thieu')
def about():
    return render_template('about.html')
@app.route('/nhuong_quyen')
def franchise():
    return render_template('franchise.html')

if __name__ == '__main__':

    app.run(debug=True)
