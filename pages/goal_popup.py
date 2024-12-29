import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from .action_popup import ActionPopup
from .add_goal_popup import AddGoalPopup
from utils.theme import set_title_bar_color  # Import set_title_bar_color function
from datetime import datetime

class GoalPopup(tk.Toplevel):
    def __init__(self, parent, project_name):
        super().__init__(parent)
        self.title("Goals for Project")
        self.transient(parent)
        self.grab_set()

        self.project_name = project_name
        self.controller = parent

        set_title_bar_color(self.controller.dark_mode)  # Set title bar color

        ttk.Label(self, text=f"Goals for Project: {project_name}", font=("Arial", 16, "bold")).pack(pady=10)

        # List of goals
        ttk.Label(self, text="Existing Goals:").pack(anchor="w", pady=5)
        self.goal_listbox = tk.Listbox(self, height=10)
        self.goal_listbox.pack(fill="both", expand=True, pady=5)
        self.goal_listbox.bind("<Double-Button-1>", self.edit_goal)  # Bind double-click event
        self.goal_listbox.bind("<Return>", self.edit_goal)  # Bind Enter key event

        # Frame for buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', pady=10)

        # Add goal button
        ttk.Button(button_frame, text="Add Goal", command=self.open_add_goal_popup).pack(side="left", padx=5)

        # Edit goal button
        ttk.Button(button_frame, text="Edit Goal", command=self.edit_goal).pack(side="left", padx=5)

        # Rename goal button
        ttk.Button(button_frame, text="Rename Goal", command=self.rename_goal).pack(side="left", padx=5)

        # Delete goal button
        ttk.Button(button_frame, text="Delete Goal", command=self.delete_goal).pack(side="left", padx=5)

        self.load_goals()

    def load_goals(self):
        self.goal_listbox.delete(0, tk.END)
        project = self.controller.projects.get(self.project_name, {})
        goals = project.get("goals", {})
        for goal_name in goals:
            self.goal_listbox.insert(tk.END, goal_name)

    def open_add_goal_popup(self):
        AddGoalPopup(self, self.project_name)
        self.load_goals()  # Update goal list after adding a new goal

    def edit_goal(self, event=None):
        selected = self.goal_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a goal.")
            return

        goal_name = self.goal_listbox.get(selected)
        goal = self.controller.projects[self.project_name]["goals"][goal_name]
        ActionPopup(self, goal_name, goal)

    def rename_goal(self):
        selected = self.goal_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a goal.")
            return

        old_name = self.goal_listbox.get(selected)
        new_name = simpledialog.askstring("Rename Goal", "Enter new goal name:", initialvalue=old_name)
        if new_name and new_name != old_name:
            if new_name in self.controller.projects[self.project_name]["goals"]:
                messagebox.showerror("Error", "Goal with this name already exists.")
                return

            self.controller.projects[self.project_name]["goals"][new_name] = self.controller.projects[self.project_name]["goals"].pop(old_name)
            self.update_goal_time(new_name)
            self.controller.save_project(self.controller.current_project)
            self.load_goals()

    def delete_goal(self):
        selected = self.goal_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a goal.")
            return

        goal_name = self.goal_listbox.get(selected)
        if messagebox.askyesno("Delete Goal", f"Are you sure you want to delete the goal '{goal_name}'?"):
            del self.controller.projects[self.project_name]["goals"][goal_name]
            self.controller.save_project(self.controller.current_project)
            self.load_goals()

    def update_goal_time(self, goal_name):
        goal = self.controller.projects[self.project_name]["goals"][goal_name]
        total_time = 0
        for action in goal["actions"].values():
            start_date = datetime.strptime(action["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(action["end_date"], "%Y-%m-%d")
            duration_weeks = (end_date - start_date).days / 7
            total_time += duration_weeks * action["weekly_time"]
        goal["GoalTime"] = total_time

        # Update project's total time
        project_total_time = sum(goal["GoalTime"] for goal in self.controller.projects[self.project_name]["goals"].values())
        self.controller.projects[self.project_name]["ProjectTime"] = project_total_time

        self.controller.save_project(self.controller.current_project)
