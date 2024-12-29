import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

class GraphPage(tk.Toplevel):
    def __init__(self, parent, project_name, project_data):
        super().__init__(parent)
        self.title(f"Weekly Summary for {project_name}")
        self.geometry("800x600")
        self.project_name = project_name
        self.project_data = project_data
        self.controller = parent.controller

        ttk.Label(self, text=f"Weekly Summary for {project_name}", font=("Arial", 16, "bold")).pack(pady=10)

        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.apply_theme()
        self.plot_graph()

    def apply_theme(self):
        if self.controller.dark_mode:
            plt.style.use('dark_background')
            self.figure.patch.set_facecolor('#333333')
            self.ax.set_facecolor('#333333')
            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['top'].set_color('white')
            self.ax.spines['right'].set_color('white')
            self.ax.spines['left'].set_color('white')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.title.set_color('white')
            self.ax.tick_params(axis='x', colors='white')
            self.ax.tick_params(axis='y', colors='white')
            self.ax.legend(frameon=False, facecolor='#333333', edgecolor='#333333')
        else:
            plt.style.use('default')
            self.figure.patch.set_facecolor('white')
            self.ax.set_facecolor('white')
            self.ax.spines['bottom'].set_color('black')
            self.ax.spines['top'].set_color('black')
            self.ax.spines['right'].set_color('black')
            self.ax.spines['left'].set_color('black')
            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')
            self.ax.title.set_color('black')
            self.ax.tick_params(axis='x', colors='black')
            self.ax.tick_params(axis='y', colors='black')
            self.ax.legend(frameon=False, facecolor='white', edgecolor='white')

    def plot_graph(self):
        weekly_summary = self.generate_weekly_summary()
        weekly_summary.plot(kind="bar", stacked=True, ax=self.ax)

        self.ax.set_title(f"Weekly Time Requirements for {self.project_name}")
        self.ax.set_xlabel("Week Number")
        self.ax.set_ylabel("Hours per Week")
        self.ax.legend(title="Actions", bbox_to_anchor=(1.05, 1), loc="upper left")
        self.figure.tight_layout()
        self.canvas.draw()

    def generate_weekly_summary(self):
        try:
            start_date = min(pd.to_datetime(action["start_date"]) for goal in self.project_data["goals"].values() for action in goal["actions"].values())
            end_date = max(pd.to_datetime(action["end_date"]) for goal in self.project_data["goals"].values() for action in goal["actions"].values())
        except ValueError:
            return pd.DataFrame()  # Return an empty DataFrame if there are no valid dates

        weekly_dates = pd.date_range(start=start_date, end=end_date, freq="W-MON")
        weekly_summary = pd.DataFrame({"Week": weekly_dates})
        weekly_summary["Week Number"] = weekly_summary["Week"].dt.isocalendar().week

        for goal in self.project_data["goals"].values():
            for action_name, action in goal["actions"].items():
                weekly_summary[action_name] = 0

        for goal in self.project_data["goals"].values():
            for action_name, action in goal["actions"].items():
                start_date = pd.to_datetime(action["start_date"])
                end_date = pd.to_datetime(action["end_date"])
                active_weeks = (weekly_summary["Week"] >= start_date) & (weekly_summary["Week"] <= end_date)
                weekly_summary.loc[active_weeks, action_name] += action["weekly_time"]

        weekly_summary.set_index("Week Number", inplace=True)
        return weekly_summary