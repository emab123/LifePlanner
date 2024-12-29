import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from pages.main_page import Main  # Import Main
from pages.goal_popup import GoalPopup
from pages.graph_page import GraphPage
from pages.add_project_popup import AddProjectPopup
from pages.preferences_page import Preferences  # Import Preferences
import os
import json
import sv_ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Goal & Action Manager")
        self.configure(bg="#333")

        # Data storage
        self.projects = {}
        self.current_project = None
        self.default_date_format = "YYYY-MM-DD"
        self.dark_mode = True

        # Apply theme
        sv_ttk.set_theme("dark")

        # Create a container for pages
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Dictionary of frames (pages)
        self.frames = {}

        for Page in (Main, Preferences):
            page_name = Page.__name__
            frame = Page(parent=self.notebook, controller=self)
            self.frames[page_name] = frame
            self.notebook.add(frame, text=page_name)

        self.show_frame("Main")

        self.load_projects()
        self.load_preferences()

    def show_frame(self, page_name):
        """Show a specific page."""
        frame = self.frames[page_name]
        self.notebook.select(frame)

    def save_project(self, project_name):
        if project_name not in self.projects:
            messagebox.showerror("Error", "Project not found.")
            return

        project_data = self.projects[project_name]
        with open(os.path.join("projects", f"{project_name}.json"), "w") as file:
            json.dump(project_data, file)
        
    def load_projects(self):
        for file in os.listdir("projects"):
            if file.endswith(".json"):
                with open(os.path.join("projects", file), "r") as f:
                    project_name = file.replace(".json", "")
                    self.projects[project_name] = json.load(f)
                    self.frames["Main"].project_tree.insert("", "end", iid=project_name, values=(project_name, self.projects[project_name].get("ProjectDescription", "")[:50], f'{self.projects[project_name].get("ProjectTime", 0):.1f}'))

    def import_project(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        with open(file_path, "r") as file:
            project_name = os.path.basename(file_path).replace(".json", "")
            self.projects[project_name] = json.load(file)
            self.frames["Main"].project_tree.insert("", "end", iid=project_name, values=(project_name, self.projects[project_name].get("ProjectDescription", "")[:50], self.projects[project_name].get("ProjectTime", 0)))

    def load_preferences(self):
        default_preferences = {
            "default_date_format": "YYYY-MM-DD",
            "dark_mode": True
        }

        if os.path.exists("preferences.json"):
            with open("preferences.json", "r") as file:
                preferences = json.load(file)
                for key, value in default_preferences.items():
                    setattr(self, key, preferences.get(key, value))
        else:
            for key, value in default_preferences.items():
                setattr(self, key, value)

        self.update_preferences()
        if self.dark_mode:
            sv_ttk.set_theme("dark")
        else:
            sv_ttk.set_theme("light")

    def save_preferences(self):
        preferences = {
            "default_date_format": self.default_date_format,
            "dark_mode": self.dark_mode
        }
        with open("preferences.json", "w") as file:
            json.dump(preferences, file)

    def update_preferences(self):
        for frame in self.frames.values():
            if hasattr(frame, 'update_preferences'):
                frame.update_preferences({
                    "default_date_format": self.default_date_format,
                    "dark_mode": self.dark_mode
                })

    def toggle_theme(self):
        if self.dark_mode:
            sv_ttk.set_theme("light")
        else:
            sv_ttk.set_theme("dark")
        self.dark_mode = not self.dark_mode
        self.update_preferences()

if __name__ == "__main__":
    app = App()
    app.mainloop()