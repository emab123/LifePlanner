import tkinter as tk
from tkinter import ttk, messagebox

class AddGoalPopup(tk.Toplevel):
    def __init__(self, parent, project_name):
        super().__init__(parent)
        self.title("Add Goal")
        self.transient(parent)
        self.grab_set()
        self.controller = parent.controller
        self.project_name = project_name

        ttk.Label(self, text="Goal Name:").pack(pady=10)
        self.goal_name_entry = ttk.Entry(self, width=50)
        self.goal_name_entry.pack(pady=10)
        self.goal_name_entry.bind("<Return>", lambda event: self.add_goal())

        ttk.Button(self, text="Add", command=self.add_goal).pack(pady=10)

        self.goal_name_entry.focus_set()

    def add_goal(self):
        goal_name = self.goal_name_entry.get().strip()
        if not goal_name:
            messagebox.showerror("Error", "Goal name cannot be empty.")
            return

        if goal_name in self.controller.projects[self.project_name]["goals"]:
            messagebox.showerror("Error", "Goal already exists.")
            return

        self.controller.projects[self.project_name]["goals"][goal_name] = {
            "actions": {},
            "GoalTime": 0
        }
        self.controller.save_project(self.project_name)
        self.controller.frames["Main"].load_goals()  # Update the goal list in the main frame
        self.destroy()