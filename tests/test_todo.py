import pytest
import json
from pathlib import Path
import tempfile
from todo_core import (
    load_tasks, save_tasks, add_task, complete_task, delete_task, get_all_tasks
)

@pytest.fixture
def temp_file():
    """Создаёт временный файл для тестов"""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        yield Path(tmp.name)
    Path(tmp.name).unlink()

@pytest.fixture
def sample_tasks():
    return [
        {"text": "Купить хлеб", "completed": False},
        {"text": "Помыть посуду", "completed": True}
    ]

def test_load_tasks_empty(temp_file):
    tasks = load_tasks(temp_file)
    assert tasks == []

def test_save_and_load(temp_file):
    tasks = [{"text": "test", "completed": False}]
    save_tasks(tasks, temp_file)
    loaded = load_tasks(temp_file)
    assert loaded == tasks

def test_add_task():
    tasks = []
    tasks = add_task(tasks, "Новая задача")
    assert len(tasks) == 1
    assert tasks[0]["text"] == "Новая задача"
    assert tasks[0]["completed"] is False

def test_add_task_empty_name():
    tasks = []
    with pytest.raises(ValueError, match="Название задачи не может быть пустым"):
        add_task(tasks, "   ")

def test_complete_task(sample_tasks):
    tasks = sample_tasks
    tasks = complete_task(tasks, 0)
    assert tasks[0]["completed"] is True

def test_complete_already_completed(sample_tasks):
    tasks = sample_tasks
    with pytest.raises(ValueError, match="Задача уже выполнена"):
        complete_task(tasks, 1)

def test_complete_invalid_index(sample_tasks):
    with pytest.raises(IndexError):
        complete_task(sample_tasks, 999)

def test_delete_task(sample_tasks):
    tasks = sample_tasks
    tasks = delete_task(tasks, 0)
    assert len(tasks) == 1
    assert tasks[0]["text"] == "Помыть посуду"

def test_delete_invalid_index(sample_tasks):
    with pytest.raises(IndexError):
        delete_task(sample_tasks, 999)

def test_get_all_tasks(sample_tasks):
    tasks = get_all_tasks(sample_tasks)
    assert tasks == sample_tasks
    # Проверка, что это копия, а не ссылка
    assert id(tasks) != id(sample_tasks)