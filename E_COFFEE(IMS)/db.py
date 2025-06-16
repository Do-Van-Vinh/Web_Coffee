# db.py
import pymysql
from pymysql.cursors import DictCursor

def MySQL_connect():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",          
        db="ecoffee_db",      # Đặt tên CSDL trong phpMyAdmin
        charset="utf8mb4",
        cursorclass=DictCursor
    )