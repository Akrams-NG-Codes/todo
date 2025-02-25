# todo.py

import json
import os
from datetime import datetime, timedelta

TODO_FILE = 'todo_list.json'
UNDO_STACK = []

def load_todo_list():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    return []

def save_todo_list(todo_list):
    with open(TODO_FILE, 'w') as file:
        json.dump(todo_list, file)

def display_todo_list(todo_list):
    if not todo_list:
        print("Your to-do list is empty.")
    else:
        print("\nTo-Do List:")
        for index, task in enumerate(todo_list, start=1):
            status = "✓" if task['completed'] else "✗"
            due_date_str = task['due_date'] if task['due_date'] else "No due date"
            print(f"{index}. [{status}] {task['task']} (Priority: {task['priority']}, Due: {due_date_str})")

def undo_last_action(todo_list):
    if UNDO_STACK:
        last_action = UNDO_STACK.pop()
        if last_action['action'] == 'add':
            todo_list.pop()
            print(f"Undo: Removed task '{last_action['task']}'")
        elif last_action['action'] == 'remove':
            todo_list.append(last_action['task'])
            print(f"Undo: Restored task '{last_action['task']['task']}'")
        save_todo_list(todo_list)
    else:
        print("No actions to undo.")

def search_tasks(todo_list, keyword):
    return [task for task in todo_list if keyword.lower() in task['task'].lower()]

def filter_tasks(todo_list, completed=None, priority=None):
    filtered_tasks = todo_list
    if completed is not None:
        filtered_tasks = [task for task in filtered_tasks if task['completed'] == completed]
    if priority:
        filtered_tasks = [task for task in filtered_tasks if task['priority'] == priority]
    return filtered_tasks

def main():
    todo_list = load_todo_list()
    
    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. View To-Do List")
        print("4. Mark Task as Completed")
        print("5. Edit Task")
        print("6. Search Tasks")
        print("7. Filter Tasks")
        print("8. Undo Last Action")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            task = input("Enter the task: ")
            priority = input("Enter priority (low, medium, high): ")
            due_date_str = input("Enter due date (YYYY-MM-DD) or leave blank: ")
            due_date = due_date_str if due_date_str else None
            new_task = {'task': task, 'completed': False, 'priority': priority, 'due_date': due_date}
            todo_list.append(new_task)
            UNDO_STACK.append({'action': 'add', 'task': new_task})
            save_todo_list(todo_list)
            print(f'Task "{task}" added.')
        
        elif choice == '2':
            display_todo_list(todo_list)
            task_num = int(input("Enter the task number to remove: ")) - 1
            if 0 <= task_num < len(todo_list):
                removed_task = todo_list.pop(task_num)
                UNDO_STACK.append({'action': 'remove', 'task': removed_task})
                save_todo_list(todo_list)
                print(f'Task "{removed_task["task"]}" removed.')
            else:
                print("Invalid task number.")
        
        elif choice == '3':
            display_todo_list(todo_list)
        
        elif choice == '4':
            display_todo_list(todo_list)
            task_num = int(input("Enter the task number to mark as completed: ")) - 1
            if 0 <= task_num < len(todo_list):
                todo_list[task_num]['completed'] = True
                save_todo_list(todo_list)
                print(f'Task "{todo_list[task_num]["task"]}" marked as completed.')
            else:
                print("Invalid task number.")
        
        elif choice == '5':
            display_todo_list(todo_list)
            task_num = int(input("Enter the task number to edit: ")) - 1
            if 0 <= task_num < len(todo_list):
                new_task = input("Enter the new task: ")
                new_priority = input("Enter new priority (low, medium, high): ")
                new_due_date_str = input("Enter new due date (YYYY-MM-DD) or leave blank: ")
                todo_list[task_num]['task'] = new_task
                todo_list[task_num]['priority'] = new_priority
                todo_list[task_num]['due_date'] = new_due_date_str if new_due_date_str else None
                save_todo_list(todo_list)
                print(f'Task updated to "{new_task}".')
            else:
                print("Invalid task number.")
        
        elif choice == '6':
            keyword = input("Enter keyword to search: ")
            results = search_tasks(todo_list, keyword)
            if results:
                print("Search Results:")
                for task in results:
                    print(f"- {task['task']} (Priority: {task['priority']})")
            else:
                print("No tasks found.")
        
        elif choice == '7':
            completed = input("Show completed tasks only? (yes/no): ").lower() == 'yes'
            priority = input("Enter priority to filter by or leave blank: ")
            filtered_tasks = filter_tasks(todo_list, completed=completed, priority=priority)
            display_todo_list(filtered_tasks)
        
        elif choice == '8':
            undo_last_action(todo_list)
        
        elif choice == '9':
            print("Exiting the To-Do List App.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()