# app.py
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'crud_db'

mysql = MySQL(app)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tbl_user(user_name, user_email) VALUES (%s, %s)", (data['name'], data['email']))
    mysql.connection.commit()
    return jsonify({"message": "User added successfully!"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_user")
    rows = cur.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
