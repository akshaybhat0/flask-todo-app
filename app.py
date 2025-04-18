import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Database configuration
def connect_db():
    return sqlite3.connect('tasks.db')

@app.route('/')
def home():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, completed FROM tasks')
    tasks = [{'id': row[0], 'name': row[1], 'completed': bool(row[2])} for row in cursor.fetchall()]
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task')
    if task_name:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (name, completed) VALUES (?, ?)', (task_name, 0))
        conn.commit()
        conn.close()
    return home()

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return home()

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return home()

if __name__ == '__main__':
    app.run(debug=True)
