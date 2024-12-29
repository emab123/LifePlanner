import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class AddActionPopup(tk.Toplevel):
    def __init__(self, parent, goal_name, action=None, action_name=None, mode="add"):
        super().__init__(parent)
        self.title(f"{'Add' if mode == 'add' else 'Edit'} Action")
        self.transient(parent)
        self.grab_set()

        self.goal_name = goal_name
        self.controller = parent.controller
        self.action = action
        self.action_name = action_name
        self.mode = mode

        date_pattern = self.controller.default_date_format.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d")

        ttk.Label(self, text="Action Name:").pack(pady=10, padx=10)
        self.action_name_entry = ttk.Entry(self, width=50)
        self.action_name_entry.pack(pady=10, padx=10)
        if self.mode == "edit":
            self.action_name_entry.insert(0, action_name)

        date_frame = ttk.Frame(self)
        date_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(date_frame, text="Start Date:").pack(side="left", padx=5)
        self.start_date_entry = DateEntry(date_frame, width=20, date_pattern=self.controller.default_date_format)
        self.start_date_entry.pack(side="left", padx=5)

        if self.mode == "edit":
            self.start_date_entry.set_date(datetime.strptime(action["start_date"], "%Y-%m-%d"))

        ttk.Label(date_frame, text="End Date:").pack(side="left", padx=5)
        self.end_date_entry = DateEntry(date_frame, width=20, date_pattern=self.controller.default_date_format)
        self.end_date_entry.pack(side="left", padx=5)

        if self.mode == "edit":
            self.end_date_entry.set_date(datetime.strptime(action["end_date"], "%Y-%m-%d"))

        ttk.Label(self, text="Weekly Time (hours):").pack(pady=10, padx=10)
        self.weekly_time_entry = ttk.Entry(self, width=50)
        self.weekly_time_entry.pack(pady=10, padx=10)
        if self.mode == "edit":
            self.weekly_time_entry.insert(0, action["weekly_time"])

        self.action_name_entry.bind("<Return>", lambda event: self.save_action())
        ttk.Button(self, text="Save", command=self.save_action).pack(pady=10, padx=10)

        self.action_name_entry.focus_set()

    def clear_and_focus(self, event):
        event.widget.focus_set()

    def validate_date(self, event):
        try:
            self.start_date_entry.get_date()
            self.end_date_entry.get_date()
        except:
            messagebox.showerror("Error", "Please select a valid date.")
            event.widget.focus_set()

    def save_action(self):
        action_name = self.action_name_entry.get().strip()
        start_date = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date_entry.get_date().strftime("%Y-%m-%d")
        weekly_time = self.weekly_time_entry.get().strip()

        if not action_name:
            messagebox.showerror("Error", "Action name cannot be empty.")
            return

        goal = self.controller.projects[self.controller.current_project]["goals"][self.goal_name]

        if self.mode == "add":
            if action_name in goal["actions"]:
                messagebox.showerror("Error", "Action already exists.")
                return
            goal["actions"][action_name] = {
                "start_date": start_date,
                "end_date": end_date,
                "weekly_time": float(weekly_time)
            }
        else:
            del goal["actions"][self.action_name]
            goal["actions"][action_name] = {
                "start_date": start_date,
                "end_date": end_date,
                "weekly_time": float(weekly_time)
            }

        self.controller.save_project(self.controller.current_project)
        self.update_goal_time(goal)
        self.master.load_actions()
        self.destroy()

    def update_goal_time(self, goal):
        total_time = 0
        for action in goal["actions"].values():
            start_date = datetime.strptime(action["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(action["end_date"], "%Y-%m-%d")
            duration_weeks = (end_date - start_date).days / 7
            total_time += duration_weeks * float(action["weekly_time"])
        goal["GoalTime"] = total_time
        self.controller.save_project(self.controller.current_project)