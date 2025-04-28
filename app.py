from flask import Flask, request, jsonify, render_template 
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Use your MySQL username here
    password="1234",  # Use your MySQL password here
    database="task"
)

@app.route('/get_task_timers', methods=['GET'])
def get_task_timers():
    cursor = db.cursor()
    cursor.execute("SELECT id, task_name, task_description, start_time, end_time, elapsed_time, status FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()

    task_data = []
    for task in tasks:
        task_id, task_name, task_description, start_time, end_time, elapsed_time, status = task
        task_data.append({
            'task_id': task_id,
            'task_name': task_name,
            'task_description': task_description,
            'start_time': start_time.isoformat() if start_time else None,
            'end_time': end_time.isoformat() if end_time else None,
            'elapsed_time': elapsed_time,
            'status': status
        })
    
    return jsonify({'tasks': task_data})

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.json['task_name']
    task_description = request.json.get('task_description', '')

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO tasks (task_name, task_description, start_time, elapsed_time, status) VALUES (%s, %s, NULL, 0, 'paused')",
        (task_name, task_description)
    )
    db.commit()
    task_id = cursor.lastrowid
    cursor.close()
    return jsonify({'task_id': task_id})

@app.route('/start_task/<int:task_id>', methods=['POST'])
def start_task(task_id):
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET start_time = %s, status = 'running' WHERE id = %s", (datetime.now(), task_id))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Task started successfully'})

@app.route('/pause_task/<int:task_id>', methods=['POST'])
def pause_task(task_id):
    cursor = db.cursor()
    cursor.execute("SELECT start_time, elapsed_time FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()

    if task and task[0]:  # if task is running
        start_time, elapsed_time = task
        new_elapsed_time = elapsed_time + int((datetime.now() - start_time).total_seconds())

        cursor.execute(
            "UPDATE tasks SET elapsed_time = %s, status = 'running' WHERE id = %s",
            (new_elapsed_time, task_id)
        )
        db.commit()
    cursor.close()
    return jsonify({'message': 'Task paused successfully'})
@app.route('/resume_task/<int:task_id>', methods=['POST'])
def resume_task(task_id):
    cursor = db.cursor()
    cursor.execute("SELECT status FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()

    if task and task[0] == 'paused':  # If the task is paused
        cursor.execute(
            "UPDATE tasks SET status = 'running' WHERE id = %s",
            (datetime.now(), task_id)
        )
        db.commit()
    cursor.close()
    return jsonify({'message': 'Task resumed successfully'})

@app.route('/stop_task/<int:task_id>', methods=['POST'])
def stop_task(task_id):
    cursor = db.cursor()
    cursor.execute("SELECT start_time, elapsed_time FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()

    if task and task[0]:  # if task is running
        start_time, elapsed_time = task
        new_elapsed_time = elapsed_time + int((datetime.now() - start_time).total_seconds())

        cursor.execute(
            "UPDATE tasks SET elapsed_time = %s, end_time = %s, status = 'stopped' WHERE id = %s",
            (new_elapsed_time, datetime.now(), task_id)
        )
        db.commit()
    cursor.close()
    return jsonify({'message': 'Task stopped successfully'})

@app.route('/remove_task/<int:task_id>', methods=['POST'])
def remove_task(task_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Task removed successfully'})

if __name__ == '__main__':
    app.run(debug=True)