import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Define the Task class
class Task:
    def __init__(self, name, description, priority, due_date):
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date
        }

# Define the TaskManager class
class TaskManager:
    def __init__(self, json_file="tasks.json"):
        self.tasks = []
        self.json_file = json_file
        self.load_tasks_from_json()

    def load_tasks_from_json(self):
        try:
            with open(self.json_file, "r") as file:
                data = json.load(file)
                self.tasks = [Task(**task) for task in data]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks_to_json(self):
        with open(self.json_file, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, name, description, priority, due_date):
        self.tasks.append(Task(name, description, priority, due_date))
        self.save_tasks_to_json()

    def update_task(self, index, name=None, description=None, priority=None, due_date=None):
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            if name:
                task.name = name
            if description:
                task.description = description
            if priority:
                task.priority = priority
            if due_date:
                task.due_date = due_date
            self.save_tasks_to_json()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks_to_json()

    def get_filtered_tasks(self, name_filter=None, priority_filter=None, due_date_filter=None):
        filtered_tasks = self.tasks
        if name_filter:
            filtered_tasks = [task for task in filtered_tasks if name_filter.lower() in task.name.lower()]
        if priority_filter:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority_filter]
        if due_date_filter:
            filtered_tasks = [task for task in filtered_tasks if task.due_date == due_date_filter]
        return filtered_tasks

    def sort_tasks(self, sort_key="name"):
        if sort_key == "name":
            self.tasks.sort(key=lambda task: task.name)
        elif sort_key == "priority":
            self.tasks.sort(key=lambda task: task.priority)
        elif sort_key == "due_date":
            self.tasks.sort(key=lambda task: task.due_date)

# Define the TaskManagerGUI class
class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Task Manager")
        self.task_manager = TaskManager()
        self.setup_gui()

    def setup_gui(self):
        # Frame for search and filter
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Search by Name:").grid(row=0, column=0, padx=5)
        self.name_filter_entry = ttk.Entry(filter_frame)
        self.name_filter_entry.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Filter by Priority:").grid(row=0, column=2, padx=5)
        self.priority_filter_combobox = ttk.Combobox(filter_frame, values=["High", "Medium", "Low"])
        self.priority_filter_combobox.grid(row=0, column=3, padx=5)

        ttk.Label(filter_frame, text="Filter by Due Date:").grid(row=0, column=4, padx=5)
        self.due_date_filter_entry = ttk.Entry(filter_frame)
        self.due_date_filter_entry.grid(row=0, column=5, padx=5)

        ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filter).grid(row=0, column=6, padx=5)

        # Treeview for displaying tasks
        self.tree = ttk.Treeview(self.root, columns=("Name", "Description", "Priority", "Due Date"), show="headings")
        self.tree.heading("Name", text="Name", command=lambda: self.sort_tasks("name"))
        self.tree.heading("Description", text="Description")
        self.tree.heading("Priority", text="Priority", command=lambda: self.sort_tasks("priority"))
        self.tree.heading("Due Date", text="Due Date", command=lambda: self.sort_tasks("due_date"))
        self.tree.pack(pady=10)

        # Buttons for CRUD operations
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Task", command=self.open_add_task_window).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Task", command=self.open_update_task_window).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5)

        # Populate the Treeview
        self.populate_tree()

    def populate_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in self.task_manager.tasks:
            self.tree.insert("", "end", values=(task.name, task.description, task.priority, task.due_date))

    def apply_filter(self):
        name_filter = self.name_filter_entry.get()
        priority_filter = self.priority_filter_combobox.get()
        due_date_filter = self.due_date_filter_entry.get()
        filtered_tasks = self.task_manager.get_filtered_tasks(name_filter, priority_filter, due_date_filter)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in filtered_tasks:
            self.tree.insert("", "end", values=(task.name, task.description, task.priority, task.due_date))

    def sort_tasks(self, sort_key):
        self.task_manager.sort_tasks(sort_key)
        self.populate_tree()

    def open_add_task_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Task")

        ttk.Label(add_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        description_entry = ttk.Entry(add_window)
        description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Priority:").grid(row=2, column=0, padx=5, pady=5)
        priority_combobox = ttk.Combobox(add_window, values=["High", "Medium", "Low"])
        priority_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        due_date_entry = ttk.Entry(add_window)
        due_date_entry.grid(row=3, column=1, padx=5, pady=5)

        def save_task():
            name = name_entry.get()
            description = description_entry.get()
            priority = priority_combobox.get()
            due_date = due_date_entry.get()
            if name and description and priority and due_date:
                self.task_manager.add_task(name, description, priority, due_date)
                self.populate_tree()
                add_window.destroy()
            else:
                messagebox.showwarning("Input Error", "All fields are required!")

        ttk.Button(add_window, text="Save", command=save_task).grid(row=4, column=0, columnspan=2, pady=10)

    def open_update_task_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a task to update!")
            return

        task_index = self.tree.index(selected_item[0])
        task = self.task_manager.tasks[task_index]

        update_window = tk.Toplevel(self.root)
        update_window.title("Update Task")

        ttk.Label(update_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(update_window)
        name_entry.insert(0, task.name)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(update_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        description_entry = ttk.Entry(update_window)
        description_entry.insert(0, task.description)
        description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(update_window, text="Priority:").grid(row=2, column=0, padx=5, pady=5)
        priority_combobox = ttk.Combobox(update_window, values=["High", "Medium", "Low"])
        priority_combobox.set(task.priority)
        priority_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(update_window, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        due_date_entry = ttk.Entry(update_window)
        due_date_entry.insert(0, task.due_date)
        due_date_entry.grid(row=3, column=1, padx=5, pady=5)

        def save_changes():
            name = name_entry.get()
            description = description_entry.get()
            priority = priority_combobox.get()
            due_date = due_date_entry.get()
            if name and description and priority and due_date:
                self.task_manager.update_task(task_index, name, description, priority, due_date)
                self.populate_tree()
                update_window.destroy()
            else:
                messagebox.showwarning("Input Error", "All fields are required!")

        ttk.Button(update_window, text="Save Changes", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a task to delete!")
            return

        task_index = self.tree.index(selected_item[0])
        self.task_manager.delete_task(task_index)
        self.populate_tree()

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()