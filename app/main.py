# app/main.py
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'crud_db')

mysql = MySQL(app)

@app.route('/users', methods=['POST'])
def add_user():
    # ... Create logic (INSERT INTO tbl_user)
    return jsonify({"message": "User added"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    # ... Read logic (SELECT * FROM tbl_user)
    return jsonify({"users": []})

# ... Add Update and Delete routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
