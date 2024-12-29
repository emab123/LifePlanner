import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from utils.theme import set_title_bar_color  # Import set_title_bar_color function
from datetime import datetime
from .add_action_popup import AddActionPopup  # Import AddActionPopup

class ActionPopup(tk.Toplevel):
    def __init__(self, parent, goal_name, goal):
        super().__init__(parent)
        self.title(f"Actions for {goal_name}")
        self.transient(parent)
        self.grab_set()
        self.parent = parent
        self.goal_name = goal_name
        self.goal = goal
        self.controller = parent.controller
        set_title_bar_color(self.controller.dark_mode)  # Set title bar color

        ttk.Label(self, text="Manage Actions", font=("Arial", 16, "bold")).pack(pady=10)

        # List of actions
        ttk.Label(self, text="Existing Actions:").pack(anchor="w", pady=5)
        self.action_tree = ttk.Treeview(self, columns=("Name", "Start Date", "End Date", "Weekly Time"), show="headings")
        self.action_tree.heading("Name", text="Name")
        self.action_tree.heading("Start Date", text="Start Date")
        self.action_tree.heading("End Date", text="End Date")
        self.action_tree.heading("Weekly Time", text="Weekly Time (hours)")
        self.action_tree.pack(fill="both", expand=True, pady=5)
        self.action_tree.bind("<Double-Button-1>", self.edit_action)
        self.action_tree.bind("<Return>", self.edit_action)

        self.load_actions()

        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=10)


        # Manage action buttons
        ttk.Button(button_frame, text="Add Action", command=self.open_add_action_popup).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Action", command=self.edit_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Rename Action", command=self.rename_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Action", command=self.delete_action).pack(side="left", padx=5)


    def open_add_action_popup(self):
        AddActionPopup(self, self.goal_name)

    def add_action(self, action_name, start_date, end_date, weekly_time):
        if not action_name:
            messagebox.showerror("Error", "Action name cannot be empty.")
            return

        if action_name in self.goal["actions"]:
            messagebox.showerror("Error", "Action already exists.")
            return

        self.goal["actions"][action_name] = {
            "start_date": start_date,
            "end_date": end_date,
            "weekly_time": weekly_time
        }
        self.update_goal_time()
        self.controller.save_project(self.controller.current_project)
        self.load_actions()

    def load_actions(self):
        self.action_tree.delete(*self.action_tree.get_children())
        for action_name in self.goal["actions"]:
            action =  self.goal["actions"][action_name]
            date_pattern = self.controller.default_date_format.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d")
            start_date = datetime.strptime(action["start_date"], "%Y-%m-%d").strftime(date_pattern)
            end_date = datetime.strptime(action["end_date"], "%Y-%m-%d").strftime(date_pattern)
            self.action_tree.insert("", "end", iid=action_name, values=(action_name, start_date, end_date, action["weekly_time"]))
        
        for col in self.action_tree["columns"]:
            max_width = tk.font.Font().measure(col)
            for row in self.action_tree.get_children():
                cell_value = self.action_tree.set(row, col)
                cell_width = tk.font.Font().measure(cell_value)
                if cell_width > max_width:
                    max_width = cell_width
            self.action_tree.column(col, width=max_width)
        
    def edit_action(self, event):
        selected = self.action_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an action.")
            return

        action_name = self.action_tree.selection()[0]
        action = self.goal["actions"][action_name]
        AddActionPopup(self, self.goal_name, action=action, action_name=action_name, mode="edit")

    def rename_action(self):
        selected = self.action_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an action.")
            return

        action_name = selected[0]
        new_name = simpledialog.askstring("Rename Action", "Enter new action name:", initialvalue=action_name)
        if new_name and new_name != action_name:
            self.goal["actions"][new_name] = self.goal["actions"].pop(action_name)
            self.update_goal_time()
            self.controller.save_project(self.controller.current_project)
            self.load_actions()

    def delete_action(self):
        selected = self.action_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an action.")
            return

        action_name = selected[0]
        if messagebox.askyesno("Delete Action", f"Are you sure you want to delete the action '{action_name}'?"):
            del self.goal["actions"][action_name]
            self.update_goal_time()
            self.controller.save_project(self.controller.current_project)
            self.load_actions()

    def update_goal_time(self):
        total_time = 0
        for action in self.goal["actions"].values():
            start_date = datetime.strptime(action["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(action["end_date"], "%Y-%m-%d")
            duration_weeks = (end_date - start_date).days / 7
            total_time += duration_weeks * float(action["weekly_time"])
        self.goal["GoalTime"] = total_time
        self.controller.save_project(self.controller.current_project)