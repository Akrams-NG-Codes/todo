import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from datetime import datetime

TODO_FILE = 'todo_list.json'
USER_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USER_FILE, 'w') as file:
        json.dump(users, file)

def load_todo_list(username):
    user_file = f"{username}_todo.json"
    if os.path.exists(user_file):
        with open(user_file, 'r') as file:
            return json.load(file)
    return []

def save_todo_list(username, todo_list):
    user_file = f"{username}_todo.json"
    with open(user_file, 'w') as file:
        json.dump(todo_list, file)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Do your list with Akrams NG Codes")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        self.users = load_users()
        self.current_user = None
        self.todo_list = []

        self.setup_login_frame()
        self.setup_todo_frame()
        self.apply_styles()

    def setup_login_frame(self):
        self.login_frame = ttk.Frame(self.root, padding="20", style="LoginFrame.TFrame")
        self.login_frame.grid(row=0, column=0, sticky="nsew")

        self.username_label = ttk.Label(self.login_frame, text="Username:", font=("Segoe UI", 12))
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = ttk.Entry(self.login_frame, font=("Segoe UI", 12))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.password_label = ttk.Label(self.login_frame, text="Password:", font=("Segoe UI", 12))
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ttk.Entry(self.login_frame, show="*", font=("Segoe UI", 12))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login, style="Advanced.TButton")
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.signup_button = ttk.Button(self.login_frame, text="Sign Up", command=self.signup, style="Advanced.TButton")
        self.signup_button.grid(row=3, column=0, columnspan=2, pady=5)

    def setup_todo_frame(self):
        self.todo_frame = ttk.Frame(self.root, padding="20", style="TodoFrame.TFrame")
        self.todo_frame.grid(row=0, column=0, sticky="nsew")

        self.task_label = ttk.Label(self.todo_frame, text="Task:", font=("Segoe UI", 12))
        self.task_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.task_entry = ttk.Entry(self.todo_frame, font=("Segoe UI", 12))
        self.task_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.due_date_label = ttk.Label(self.todo_frame, text="Due Date (DD/MM/YY):", font=("Segoe UI", 12))
        self.due_date_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.due_date_entry = ttk.Entry(self.todo_frame, font=("Segoe UI", 12))
        self.due_date_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.priority_label = ttk.Label(self.todo_frame, text="Priority:", font=("Segoe UI", 12))
        self.priority_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_dropdown = ttk.Combobox(self.todo_frame, textvariable=self.priority_var,
                                               values=["High", "Medium", "Low"], state="readonly", font=("Segoe UI", 12))
        self.priority_dropdown.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        self.add_task_button = ttk.Button(self.todo_frame, text="Add Task", command=self.add_task, style="Advanced.TButton")
        self.add_task_button.grid(row=0, column=6, padx=5, pady=5)

        self.task_frame = ttk.Frame(self.todo_frame)
        self.task_frame.grid(row=1, columnspan=7, sticky="nsew")

        self.task_listbox = tk.Listbox(self.task_frame, selectmode=tk.SINGLE, font=("Segoe UI", 12), width=60)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.edit_task_button = ttk.Button(self.todo_frame, text="Edit Task", command=self.edit_task, style="Advanced.TButton")
        self.edit_task_button.grid(row=2, column=0, padx=5, pady=5)

        self.delete_task_button = ttk.Button(self.todo_frame, text="Delete Task", command=self.delete_task, style="Advanced.TButton")
        self.delete_task_button.grid(row=2, column=1, padx=5, pady=5)

        self.mark_completed_button = ttk.Button(self.todo_frame, text="Mark Completed", command=self.mark_completed, style="Advanced.TButton")
        self.mark_completed_button.grid(row=2, column=2, padx=5, pady=5)

        self.search_label = ttk.Label(self.todo_frame, text="Search:", font=("Segoe UI", 12))
        self.search_label.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(self.todo_frame, font=("Segoe UI", 12))
        self.search_entry.grid(row=2, column=4, padx=5, pady=5, sticky="ew")
        self.search_button = ttk.Button(self.todo_frame, text="Search", command=self.search_task, style="Advanced.TButton")
        self.search_button.grid(row=2, column=5, padx=5, pady=5)

        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.todo_frame.grid_rowconfigure(1, weight=1)
        self.todo_frame.grid_columnconfigure(1, weight=1)
        self.todo_frame.grid_columnconfigure(3, weight=1)
        self.todo_frame.grid_columnconfigure(4, weight=1)
        self.todo_frame.grid_columnconfigure(5, weight=1)

    def apply_styles(self):
        style = ttk.Style()
        style.configure("LoginFrame.TFrame", background="#f0f0f0")
        style.configure("TodoFrame.TFrame", background="#ffffff")
        style.configure("TButton", padding=6)
        style.configure("TLabel", background="#f0f0f0")
        style.configure("TCombobox", padding=6)

        # Advanced Button Styles
        style.configure("Advanced.TButton", background="#007BFF", foreground="black", font=("Segoe UI", 10, "bold"), borderwidth=2)
        style.map("Advanced.TButton",
                  background=[("active", "#0056b3")],
                  relief=[("pressed", "sunken"), ("!pressed", "raised")])

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.todo_list = load_todo_list(username)
            self.update_task_list()
            messagebox.showinfo("Login", "Login successful!")
            self.login_frame.grid_forget()
            self.todo_frame.grid(sticky="nsew")
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users:
            messagebox.showerror("Sign Up", "User already exists.")
        else:
            self.users[username] = password
            save_users(self.users)
            messagebox.showinfo("Sign Up", "User created successfully.")

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_var.get()
        
        # Validate and parse the due date
        try:
            due_date_obj = datetime.strptime(due_date, "%d/%m/%y")
            due_date = due_date_obj.strftime("%d/%m/%y")  # Store in desired format
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter the due date in the format DD/MM/YY.")
            return

        if task:
            self.todo_list.append({'task': task, 'completed': False, 'due_date': due_date, 'priority': priority})
            save_todo_list(self.current_user, self.todo_list)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.todo_list[selected_index[0]]
            new_task = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=task['task'])
            new_due_date = simpledialog.askstring("Edit Due Date", "Edit due date (DD/MM/YY):", initialvalue=task['due_date'])
            new_priority = simpledialog.askstring("Edit Priority", "Edit priority (High, Medium, Low):", initialvalue=task['priority'])
            
            # Validate and parse the due date
            try:
                due_date_obj = datetime.strptime(new_due_date, "%d/%m/%y")
                new_due_date = due_date_obj.strftime("%d/%m/%y")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter the due date in the format DD/MM/YY.")
                return

            if new_task:
                task['task'] = new_task
                task['due_date'] = new_due_date
                task['priority'] = new_priority
                save_todo_list(self.current_user, self.todo_list)
                self.update_task_list()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            del self.todo_list[selected_index[0]]
            save_todo_list(self.current_user, self.todo_list)
            self.update_task_list()

    def mark_completed(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.todo_list[selected_index[0]]['completed'] = True
            save_todo_list(self.current_user, self.todo_list)
            self.update_task_list()

    def search_task(self):
        keyword = self.search_entry.get()
        filtered_tasks = [task for task in self.todo_list if keyword.lower() in task['task'].lower()]
        self.task_listbox.delete(0, tk.END)
        for task in filtered_tasks:
            self.task_listbox.insert(tk.END, task['task'])

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.todo_list:
            due_date = task['due_date']
            if due_date and datetime.strptime(due_date, '%d/%m/%y') < datetime.now() and not task['completed']:
                display_text = f"✗ {task['task']} (Due: {due_date}) [OVERDUE]"
            else:
                display_text = f"{'✓' if task['completed'] else '✗'} {task['task']} (Due: {due_date})"
            self.task_listbox.insert(tk.END, display_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()