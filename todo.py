import json
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = Path("tasks.json")

# Загрузка задач из файла
if file_path.exists() and file_path.stat().st_size > 0:
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            tasks = []
            print(f"Ошибка: файл {file_path} поврежден. Создан новый список задач.")
else:
    tasks = []
    print(f"Файл {file_path} не найден или пуст. Создан новый список задач.")


def print_menu():
    print("\n--- Главное меню ---")
    print("1. Добавить задачу")
    print("2. Показать задачи")
    print("3. Отметить задачу выполненной")
    print("4. Удалить задачу")
    print("5. Выйти")
    print("-----------------")


def save_tasks(tasks_list):
    """Сохраняет список задач в файл"""
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(tasks_list, json_file, ensure_ascii=False, indent=2)


def task_add(tasks_list):
    name = input("Какую задачу вы хотите добавить? ")
    if name.strip() == "":
        print("Ошибка: задача не может быть пустой")
        return tasks_list

    tasks_list.append({"text": name, "completed": False})
    save_tasks(tasks_list)
    print(f"Задача '{name}' добавлена")
    return tasks_list


def task_show(tasks_list):
    if len(tasks_list) == 0:
        print('Задач в списке нет')
        return

    print("\n--- Список задач ---")
    for index, task in enumerate(tasks_list):
        status = "✅" if task["completed"] else "❌"
        print(f"{index + 1}: {status} {task['text']}")
    print("---------------------")


def task_complete(tasks_list):
    if len(tasks_list) == 0:
        print("Нет задач для выполнения")
        return tasks_list

    task_show(tasks_list)

    while True:
        try:
            num = int(input("Какую задачу вы уже выполнили? Введите номер: "))
            if 1 <= num <= len(tasks_list):
                break
            else:
                print(f"Ошибка: введите число от 1 до {len(tasks_list)}")
        except ValueError:
            print("Ошибка: введите число, а не буквы")

    if tasks_list[num - 1]["completed"]:
        print("Эта задача уже была выполнена")
    else:
        tasks_list[num - 1]["completed"] = True
        save_tasks(tasks_list)
        print(f"Задача '{tasks_list[num - 1]['text']}' отмечена как выполненная ✅")

    return tasks_list


def task_delete(tasks_list):
    if len(tasks_list) == 0:
        print("Нет задач для удаления")
        return tasks_list

    task_show(tasks_list)

    while True:
        try:
            num = int(input("Какую задачу вы хотите удалить? Введите номер: "))
            if 1 <= num <= len(tasks_list):
                break
            else:
                print(f"Ошибка: введите число от 1 до {len(tasks_list)}")
        except ValueError:
            print("Ошибка: введите число, а не буквы")

    deleted_text = tasks_list[num - 1]["text"]
    del tasks_list[num - 1]
    save_tasks(tasks_list)
    print(f"Задача '{deleted_text}' удалена")

    return tasks_list


# Основной цикл
print_menu()

while True:
    choice = input("\nВведите цифру (1-5): ")

    if choice == '1':
        tasks = task_add(tasks)
    elif choice == '2':
        task_show(tasks)
    elif choice == '3':
        tasks = task_complete(tasks)
    elif choice == '4':
        tasks = task_delete(tasks)
    elif choice == '5':
        print("До свидания!")
        break
    else:
        print("Ошибка: введите цифру от 1 до 5")