import sys
import io
from pathlib import Path
from todo_core import load_tasks, save_tasks, add_task, complete_task, delete_task, get_all_tasks

# Настройка кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILE_PATH = Path("tasks.json")
tasks = load_tasks(FILE_PATH)


def print_menu():
    print("\n--- Меню задач ---")
    print("1. Добавить задачу")
    print("2. Показать задачи")
    print("3. Отметить выполненной")
    print("4. Удалить задачу")
    print("5. Выход")
    print("-----------------")


def print_tasks(tasks_list):
    """Отображает список задач с индексами и статусом"""
    if not tasks_list:
        print('📭 Нет задач в списке')
        return

    print("\n--- Список задач ---")
    for idx, task in enumerate(tasks_list):
        status = "✅" if task["completed"] else "⭕"
        print(f"{idx + 1}: {status} {task['text']}")
    print("---------------------")


def main():
    print_menu()

    while True:
        choice = input("\nВыберите действие (1-5): ")

        if choice == '1':
            name = input("Введите название задачи: ")
            try:
                global tasks
                tasks = add_task(tasks, name)
                save_tasks(tasks, FILE_PATH)
                print(f"✅ Задача '{name}' добавлена")
            except ValueError as e:
                print(f"❌ Ошибка: {e}")

        elif choice == '2':
            print_tasks(tasks)

        elif choice == '3':
            if not tasks:
                print("📭 Нет задач для отметки")
                continue

            print_tasks(tasks)
            try:
                num = int(input("Номер задачи для отметки: "))
                tasks = complete_task(tasks, num - 1)
                save_tasks(tasks, FILE_PATH)
                print("✅ Задача отмечена как выполненная")
            except ValueError:
                print("❌ Ошибка: введите число")
            except IndexError:
                print(f"❌ Ошибка: введите число от 1 до {len(tasks)}")

        elif choice == '4':
            if not tasks:
                print("📭 Нет задач для удаления")
                continue

            print_tasks(tasks)
            try:
                num = int(input("Номер задачи для удаления: "))
                tasks = delete_task(tasks, num - 1)
                save_tasks(tasks, FILE_PATH)
                print("🗑️ Задача удалена")
            except ValueError:
                print("❌ Ошибка: введите число")
            except IndexError:
                print(f"❌ Ошибка: введите число от 1 до {len(tasks)}")

        elif choice == '5':
            print("👋 До свидания!")
            break

        else:
            print("❌ Ошибка: введите число от 1 до 5")


if __name__ == "__main__":
    main()