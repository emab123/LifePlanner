import tkinter as tk
from tkinter import ttk, messagebox

class AddProjectPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Project")
        self.transient(parent)
        self.grab_set()
        self.controller = parent.controller  # Ensure the controller is the main application class

        ttk.Label(self, text="Project Name:").pack(pady=10)
        self.project_name_entry = ttk.Entry(self, width=50)
        self.project_name_entry.pack(pady=10)
        self.project_name_entry.bind("<Return>", lambda event: self.add_project())

        ttk.Button(self, text="Add", command=self.add_project).pack(pady=10)

        self.project_name_entry.focus_set()

    def add_project(self):
        project_name = self.project_name_entry.get().strip()
        if not project_name:
            messagebox.showerror("Error", "Project name cannot be empty.")
            return

        if project_name in self.controller.projects:
            messagebox.showerror("Error", "Project already exists.")
            return

        self.controller.projects[project_name] = {
            "goals": {},
            "ProjectDescription": "",
            "ProjectTime": 0
        }
        self.controller.frames["Main"].project_tree.insert("", "end", iid=project_name, values=(project_name, "", 0))
        self.controller.save_project(project_name)
        self.destroy()