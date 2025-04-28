# 📝 Task Timer API with Flask and MySQL

This is a **Flask**-based backend application that allows you to manage tasks with start, pause, resume, stop, and remove functionality, storing task information in a **MySQL** database.

## 📋 Features
- Add new tasks
- Start a task timer
- Pause a running task
- Resume a paused task
- Stop a task and save its elapsed time
- Remove a task
- Fetch all tasks with their status and timer details

## 🏗️ Project Structure
```
.
├── app.py          # Flask application with API endpoints
├── templates/
│   └── index.html  # (Optional) HTML template to display tasks
└── README.md       # Project documentation
```

## 🛠️ Setup Instructions

### 1. Install Python packages
Make sure you have **Python 3** installed. Then install Flask and MySQL Connector:
```bash
pip install flask mysql-connector-python
```

### 2. Setup MySQL Database
Create a MySQL database named `task` and a table called `tasks`:

```sql
CREATE DATABASE task;

USE task;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    task_description TEXT,
    start_time DATETIME,
    end_time DATETIME,
    elapsed_time INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'paused'
);
```

Update your database connection details in the `app.py` file:
```python
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Your MySQL username
    password="1234",  # Your MySQL password
    database="task"
)
```

### 3. Run the Application
```bash
python app.py
```

The app will be running at:
```
http://127.0.0.1:5000/
```

## 📚 API Endpoints

| Method | Endpoint                  | Description                   |
|:------:|----------------------------|-------------------------------|
| GET    | `/get_task_timers`          | Get all tasks with their details |
| GET    | `/`                         | Render HTML page (index.html) with all tasks |
| POST   | `/add_task`                 | Add a new task (`task_name`, `task_description`) |
| POST   | `/start_task/<task_id>`      | Start a specific task |
| POST   | `/pause_task/<task_id>`      | Pause a specific task |
| POST   | `/resume_task/<task_id>`     | Resume a paused task |
| POST   | `/stop_task/<task_id>`       | Stop and finalize a task |
| POST   | `/remove_task/<task_id>`     | Remove a task permanently |

## 📦 Example JSON Payloads

### Add a New Task
```json
POST /add_task
{
    "task_name": "Write Documentation",
    "task_description": "Prepare README file for the project."
}
```

### Expected Response
```json
{
    "task_id": 1
}
```

---

## 🔥 Notes
- Ensure your MySQL server is running before starting the app.
- `elapsed_time` is stored in **seconds**.
- The `index.html` file is optional and can be customized to view tasks visually.

---

## 📜 License
This project is licensed under the [MIT License](LICENSE) - feel free to use it and modify it as needed!

