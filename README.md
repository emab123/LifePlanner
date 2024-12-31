# Life Planner

Life Planner is a Python-based application that helps you manage your projects, goals, and actions. It provides a graphical user interface (GUI) to add, edit, and delete projects, goals, and actions. The application also supports dark mode and allows you to generate weekly summary graphs for your projects.

## Features

- **Manage Projects**: Add, edit, rename, delete, and import projects.
- **Manage Goals**: Add, edit, rename, and delete goals within a project.
- **Manage Actions**: Add, edit, rename, and delete actions within a goal.
- **Weekly Summary Graph**: Generate and display a stacked bar graph showing the weekly time requirements for a project.
- **Preferences**: Customize the default date format and toggle dark mode.

## Why Life Planner?

Life Planner helps students and programmers manage their time effectively by:
- Breaking down long-term goals into manageable weekly actions
- Visualizing time commitments with stacked bar graphs
- Balancing multiple projects and goals simultaneously
- Tracking progress over academic terms or project timelines

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/life-planner.git
    cd life-planner
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```sh
    python main.py
    ```

## Project Structure

```
life-planner/
├── .gitignore
├── main.py
├── pages/
│   ├── __init__.py
│   ├── action_popup.py
│   ├── add_action_popup.py
│   ├── add_goal_popup.py
│   ├── add_project_popup.py
│   ├── goal_popup.py
│   ├── graph_page.py
│   ├── main_page.py
│   ├── preferences_page.py
├── preferences.json
├── projects/
│   └── 2025.json
├── requirements.txt
└── utils/
    ├── __init__.py
    └── theme.py
```

## Usage

### Main Window

The main window contains a list of existing projects and buttons to manage projects:

- **Open Project**: Open the selected project to manage its goals.
- **Add Project**: Open a popup to add a new project.
- **Rename Project**: Rename the selected project.
- **Delete Project**: Delete the selected project.
- **Import Project**: Import a project from a JSON file.
- **Generate Graph**: Generate a weekly summary graph for the selected project.

### Preferences

The preferences tab allows you to customize the default date format and toggle dark mode.

### Goals and Actions

Within a project, you can manage goals and actions:

- **Add Goal**: Add a new goal to the project.
- **Edit Goal**: Edit the selected goal.
- **Rename Goal**: Rename the selected goal.
- **Delete Goal**: Delete the selected goal.
- **Add Action**: Add a new action to the goal.
- **Edit Action**: Edit the selected action.
- **Rename Action**: Rename the selected action.
- **Delete Action**: Delete the selected action.

### Weekly Summary Graph

Generate a stacked bar graph showing the weekly time requirements for a project. The x-axis represents the week number, and the y-axis represents the hours per week.

## Developer Guide

### Architecture
The application follows a modular architecture:
- `main.py`: Application entry point and core functionality
- `pages/`: UI components for different views
- `utils/`: Helper functions and theme management

### Creating Extensions
You can extend Life Planner by:
1. Adding new visualization types in `pages/graph_page.py`
2. Creating custom importers for different data formats
3. Implementing additional statistics and analytics
4. Adding new theme options

### Example: Creating a Custom Graph
```python
class CustomGraph(GraphPage):
    def plot_graph(self):
        # Your custom visualization code here
        pass
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI.
- [Matplotlib](https://matplotlib.org/) for generating graphs.
- [Pandas](https://pandas.pydata.org/) for data manipulation.
- [sv_ttk](https://github.com/rdbende/Sun-Valley-ttk-theme) for the dark mode theme.