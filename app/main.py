import os
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database config from environment variables
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "todoapp")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "tododb")

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Initialise table if not exists
def init_db():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    with conn.cursor() as c:
        c.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
    conn.close()

    conn = get_db()
    with conn.cursor() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE
            )
        """)
        conn.commit()
    conn.close()

@app.route('/todos', methods=['GET'])
def list_todos():
    conn = get_db()
    with conn.cursor() as c:
        c.execute("SELECT * FROM todos")
        todos = c.fetchall()
    conn.close()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    conn = get_db()
    with conn.cursor() as c:
        c.execute("INSERT INTO todos (title) VALUES (%s)", (data['title'],))
        conn.commit()
        new_id = c.lastrowid
    conn.close()
    return jsonify({"id": new_id, "title": data['title'], "completed": False}), 201

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    conn = get_db()
    with conn.cursor() as c:
        c.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        todo = c.fetchone()
    conn.close()
    if todo:
        return jsonify(todo)
    return jsonify({"error": "Not found"}), 404

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    conn = get_db()
    with conn.cursor() as c:
        c.execute(
            "UPDATE todos SET title = %s, completed = %s WHERE id = %s",
            (data['title'], data.get('completed', False), todo_id)
        )
        conn.commit()
    conn.close()
    return jsonify({"id": todo_id, "title": data['title'], "completed": data.get('completed', False)})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = get_db()
    with conn.cursor() as c:
        c.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        conn.commit()
    conn.close()
    return jsonify({"success": True})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)
