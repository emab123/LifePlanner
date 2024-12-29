import tkinter as tk
from tkinter import ttk, messagebox

class Preferences(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=20)

        ttk.Label(self, text="Preferences", font=("Arial", 16, "bold")).pack(pady=10)

        # Default date format
        ttk.Label(self, text="Default Date Format:").pack(anchor="w", pady=5)
        self.date_format_var = tk.StringVar(value=self.controller.default_date_format)
        self.date_format_dropdown = ttk.Combobox(self, textvariable=self.date_format_var, values=["YYYY-MM-DD", "DD-MM-YYYY", "MM-DD-YYYY"])
        self.date_format_dropdown.pack(fill="x", pady=5)

        # Dark mode toggle
        self.dark_mode_var = tk.BooleanVar(value=self.controller.dark_mode)
        ttk.Checkbutton(self, text="Enable Dark Mode", variable=self.dark_mode_var, command=self.toggle_dark_mode).pack(pady=10)

    def toggle_dark_mode(self):
        self.controller.toggle_theme()

    def save_preferences(self):
        self.controller.default_date_format = self.date_format_var.get().strip()
        self.controller.dark_mode = self.dark_mode_var.get()
        self.controller.save_preferences()