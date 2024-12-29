import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pages.goal_popup import GoalPopup  # Import GoalPopup
from pages.add_project_popup import AddProjectPopup  # Import AddProjectPopup
from pages.graph_page import GraphPage  # Import GraphPage

class Main(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(padding=20)

        ttk.Label(self, text="Manage Projects", font=("Arial", 16, "bold")).pack(pady=10)

        # Treeview for projects
        columns = ("Name", "Description", "Total Time")
        self.project_tree = ttk.Treeview(self, columns=columns, show="headings")
        self.project_tree.heading("Name", text="Name")
        self.project_tree.heading("Description", text="Description")
        self.project_tree.heading("Total Time", text="Total Time (hours)")
        self.project_tree.pack(fill="both", expand=True, pady=5)
        self.project_tree.bind("<Double-Button-1>", self.open_project)  # Bind double-click event
        self.project_tree.bind("<Return>", self.open_project)  # Bind Enter key event

        # Frame for buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        # First row of buttons
        first_row = ttk.Frame(button_frame)
        first_row.pack(fill="x", pady=5)

        # Second row of buttons
        second_row = ttk.Frame(button_frame)
        second_row.pack(fill="x", pady=5)

        ttk.Button(first_row, text="Open Project", command=self.open_project).pack(side="left", padx=5)
        ttk.Button(first_row, text="Delete Project", command=self.delete_project).pack(side="left", padx=5)
        ttk.Button(first_row, text="Rename Project", command=self.rename_project).pack(side="left", padx=5)
        ttk.Button(second_row, text="Add Project", command=self.open_add_project_popup).pack(side="left", padx=5)
        ttk.Button(second_row, text="Import Project", command=self.import_project).pack(side="left", padx=5)
        ttk.Button(second_row, text="Generate Graph", command=self.generate_graph).pack(side="left", padx=5)
        self.load_projects()

    def load_projects(self):
        for project_name, project_data in self.controller.projects.items():
            description = project_data.get("ProjectDescription", "")
            total_time = project_data.get("ProjectTime", 0)
            self.project_tree.insert("", "end", iid=project_name, values=(project_name, description[:50], total_time))

    def open_add_project_popup(self):
        AddProjectPopup(self)

    def open_project(self, event=None):
        selected = self.project_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a project.")
            return

        project_name = selected[0]
        self.controller.current_project = project_name
        GoalPopup(self.controller, project_name)

    def rename_project(self):
        selected = self.project_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a project.")
            return

        old_name = selected[0]
        new_name = simpledialog.askstring("Rename Project", "Enter new project name:", initialvalue=old_name)
        if new_name and new_name != old_name:
            if new_name in self.controller.projects:
                messagebox.showerror("Error", "Project with this name already exists.")
                return

            self.controller.projects[new_name] = self.controller.projects.pop(old_name)
            self.controller.save_project(new_name)
            self.project_tree.delete(old_name)
            self.project_tree.insert("", "end", iid=new_name, values=(new_name, self.controller.projects[new_name].get("ProjectDescription", "")[:50], self.controller.projects[new_name].get("ProjectTime", 0)))
            if self.controller.current_project == old_name:
                self.controller.current_project = new_name

    def delete_project(self):
        selected = self.project_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a project.")
            return

        project_name = selected[0]
        if messagebox.askyesno("Delete Project", f"Are you sure you want to delete the project '{project_name}'?"):
            del self.controller.projects[project_name]
            self.project_tree.delete(project_name)
            if self.controller.current_project == project_name:
                self.controller.current_project = None
            os.remove(os.path.join(self.controller.project_folder, f"{project_name}.json"))

    def import_project(self):
        self.controller.import_project()

    def generate_graph(self):
        selected = self.project_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a project.")
            return

        project_name = selected[0]
        project_data = self.controller.projects.get(project_name)
        if not project_data:
            messagebox.showerror("Error", "Project data not found.")
            return

        GraphPage(self, project_name, project_data)
