from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from todo_core import load_tasks, save_tasks, add_task, complete_task, delete_task

app = FastAPI(title="Todo List Web")

FILE_PATH = Path("tasks.json")
tasks = load_tasks(FILE_PATH)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo List</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .add-form {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        .add-form input {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
        }
        .add-form input:focus {
            outline: none;
            border-color: #667eea;
        }
        .add-form button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
        }
        .add-form button:hover {
            opacity: 0.9;
        }
        .task-list {
            list-style: none;
        }
        .task-item {
            display: flex;
            align-items: center;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .task-status {
            width: 24px;
            height: 24px;
            margin-right: 12px;
            cursor: pointer;
            font-size: 20px;
            background: none;
            border: none;
        }
        .task-text {
            flex: 1;
            font-size: 16px;
        }
        .task-text.completed {
            text-decoration: line-through;
            color: #888;
        }
        .delete-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
        }
        .delete-btn:hover {
            background: #c82333;
        }
        .empty {
            text-align: center;
            color: #888;
            padding: 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Todo List</h1>
        <form class="add-form" action="/add" method="post">
            <input type="text" name="title" placeholder="Новая задача..." required>
            <button type="submit">Добавить</button>
        </form>
        <div id="task-list"></div>
    </div>
    <script>
        async function loadTasks() {
            const response = await fetch('/api/tasks');
            const tasks = await response.json();
            const container = document.getElementById('task-list');
            if (tasks.length === 0) {
                container.innerHTML = '<div class="empty">📭 Нет задач. Добавьте первую!</div>';
                return;
            }
            let html = '<ul class="task-list">';
            for (let i = 0; i < tasks.length; i++) {
                const task = tasks[i];
                const completedClass = task.completed ? 'completed' : '';
                const statusIcon = task.completed ? '✅' : '⭕';
                html += '<li class="task-item">';
                html += '<form action="/complete/' + i + '" method="post" style="margin:0">';
                html += '<button type="submit" class="task-status">' + statusIcon + '</button>';
                html += '</form>';
                html += '<span class="task-text ' + completedClass + '">' + escapeHtml(task.text) + '</span>';
                html += '<form action="/delete/' + i + '" method="post" style="margin:0">';
                html += '<button type="submit" class="delete-btn">🗑️</button>';
                html += '</form>';
                html += '</li>';
            }
            html += '</ul>';
            container.innerHTML = html;
        }
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        loadTasks();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=HTML_TEMPLATE)

@app.get("/api/tasks")
async def get_tasks():
    return tasks

@app.post("/add")
async def add(title: str = Form(...)):
    global tasks
    try:
        tasks = add_task(tasks, title)
        save_tasks(tasks, FILE_PATH)
    except ValueError:
        pass
    return RedirectResponse(url="/", status_code=303)

@app.post("/complete/{task_id}")
async def complete(task_id: int):
    global tasks
    try:
        tasks = complete_task(tasks, task_id)
        save_tasks(tasks, FILE_PATH)
    except (IndexError, ValueError):
        pass
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{task_id}")
async def delete(task_id: int):
    global tasks
    try:
        tasks = delete_task(tasks, task_id)
        save_tasks(tasks, FILE_PATH)
    except IndexError:
        pass
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
