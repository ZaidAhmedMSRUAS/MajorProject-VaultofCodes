import tkinter as tk
from tkinter import messagebox
import json

class Zaid:
    def __init__(self, title, des, cat):
        self.title = title
        self.description = des
        self.category = cat
        self.completed = False

    def mark_completed(self):
        self.completed = True

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return [Zaid(**data) for data in json.load(f)]
    except FileNotFoundError:
        return []

class Project:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application Project @ VaultofCodes")
        self.root.geometry("600x600")  # Set window size

        # Background Color
        self.root.configure(bg="#ADD8E6")  # Light blue background

        # Frame for Task List
        self.task_frame = tk.Frame(self.root, bg="#ADD8E6")  # frame background
        self.task_frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.task_frame, height=15, width=50, font=("Times New Roman", 15), selectmode=tk.SINGLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        # Frame for Input Fields
        self.input_frame = tk.Frame(self.root, bg="#ADD8E6")  # blue frame background
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Title:", font=("Times New Roman", 15), bg="#ADD8E6").grid(row=0, column=0, padx=5)
        self.title_entry = tk.Entry(self.input_frame, width=40, font=("Times New Roman", 15))
        self.title_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.input_frame, text="Description:", font=("Times New Roman", 15), bg="#ADD8E6").grid(row=1, column=0, padx=5)
        self.description_entry = tk.Entry(self.input_frame, width=40, font=("Times New Roman", 15))
        self.description_entry.grid(row=1, column=1, padx=5)

        tk.Label(self.input_frame, text="Category:", font=("Times New Roman", 15), bg="#ADD8E6").grid(row=2, column=0, padx=5)
        self.category_entry = tk.Entry(self.input_frame, width=40, font=("Times New Roman", 15))
        self.category_entry.grid(row=2, column=1, padx=5)

        # Frame for Buttons
        self.button_frame = tk.Frame(self.root, bg="#ADD8E6")  # blue frame background
        self.button_frame.pack(pady=10)

        self.add_task_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task, width=15, font=("Times New Roman", 15))
        self.add_task_button.grid(row=0, column=0, padx=5)

        self.complete_task_button = tk.Button(self.button_frame, text="Mark Completed", command=self.complete_task, width=15, font=("Times New Roman", 15))
        self.complete_task_button.grid(row=0, column=1, padx=5)

        self.delete_task_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task, width=15, font=("Times New Roman", 15))
        self.delete_task_button.grid(row=0, column=2, padx=5)

        self.tasks = load_tasks()
        self.refresh_task_list()

    def refresh_task_list(self):
        """Refresh the task list in the listbox"""
        self.task_listbox.delete(0, tk.END)
        for index, task in enumerate(self.tasks):
            status = "Completed" if task.completed else "Pending"
            self.task_listbox.insert(tk.END, f"{index + 1}. {task.title} - {task.category} - {status}")

    def add_task(self):
        """Add a new task"""
        title = self.title_entry.get()
        description = self.description_entry.get()
        category = self.category_entry.get()

        if title and category:  # Ensure task has a title and category
            new_task = Zaid(title, description, category)
            self.tasks.append(new_task)
            save_tasks(self.tasks)
            self.refresh_task_list()
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill in both the title and category.")

    def complete_task(self):
        """Mark the selected task as completed"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index].mark_completed()
            save_tasks(self.tasks)
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def delete_task(self):
        """Delete the selected task"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            save_tasks(self.tasks)
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Selection Error", "Select at least one task to delete.")

    def clear_entries(self):
        """Clear input fields after adding a task"""
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = Project(root)
    root.mainloop()