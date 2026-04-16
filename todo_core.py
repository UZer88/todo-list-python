import json
from pathlib import Path
from typing import List, Dict

def load_tasks(file_path: Path) -> List[Dict]:
    """Загружает задачи из JSON-файла"""
    if file_path.exists() and file_path.stat().st_size > 0:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks_list: List[Dict], file_path: Path) -> None:
    """Сохраняет задачи в JSON-файл"""
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(tasks_list, json_file, ensure_ascii=False, indent=2)

def add_task(tasks_list: List[Dict], name: str) -> List[Dict]:
    """Добавляет новую задачу"""
    if not name.strip():
        raise ValueError("Название задачи не может быть пустым")
    tasks_list.append({"text": name.strip(), "completed": False})
    return tasks_list

def complete_task(tasks_list: List[Dict], index: int) -> List[Dict]:
    """Отмечает задачу выполненной"""
    if index < 0 or index >= len(tasks_list):
        raise IndexError("Неверный индекс задачи")
    if tasks_list[index]["completed"]:
        raise ValueError("Задача уже выполнена")
    tasks_list[index]["completed"] = True
    return tasks_list

def delete_task(tasks_list: List[Dict], index: int) -> List[Dict]:
    """Удаляет задачу"""
    if index < 0 or index >= len(tasks_list):
        raise IndexError("Неверный индекс задачи")
    del tasks_list[index]
    return tasks_list

def get_all_tasks(tasks_list: List[Dict]) -> List[Dict]:
    """Возвращает список всех задач"""
    return tasks_list.copy()