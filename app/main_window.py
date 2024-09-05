from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QSplitter, QTextEdit

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyQT Todo App")
        self._init_widgets()

    def _init_widgets(self) -> None:
        h_layout = QHBoxLayout(self)

        topleft = QFrame()
        topleft.setFrameShape(QFrame.StyledPanel)
        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)

        splitter1 = QSplitter(Qt.Orientation.Horizontal)
        textedit = QTextEdit()
        splitter1.addWidget(topleft)
        splitter1.addWidget(textedit)
        splitter1.setSizes([100,200])

        splitter2 = QSplitter(Qt.Orientation.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        h_layout.addWidget(splitter2)

        self.setLayout(h_layout)
        self.setFixedSize(QSize(800, 480))


import json
import os
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QSplitter, QTextEdit, QListWidget, QPushButton, QInputDialog, QApplication

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyQT Todo App")
        self._todos = []  # List to store todos
        self._file_path = "todos.json"  # File to store todos
        self._init_widgets()
        self._load_todos()  # Load todos from file

    def _init_widgets(self) -> None:
        # Initialize frames and text editor
        top_frame = self._create_frame("background-color: lightblue;")
        bottom_frame = self._create_frame("background-color: lightgreen;")

        # Add list widget and new todo button to the top frame
        self.todo_list = QListWidget()
        self.todo_list.itemClicked.connect(self._display_todo)
        add_todo_button = QPushButton("Add Todo")
        add_todo_button.clicked.connect(self._add_todo)

        top_layout = QVBoxLayout()
        top_layout.addWidget(add_todo_button)
        top_layout.addWidget(self.todo_list)
        top_frame.setLayout(top_layout)

        # Text editor for viewing/editing todo
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("background-color: lightyellow; color: black")
        self.text_edit.setDisabled(True) # Disable the text edit initially
        self.text_edit.textChanged.connect(self._update_todo)

        # Create the first splitter (horizontal)
        horizontal_splitter = QSplitter(Qt.Orientation.Horizontal)
        horizontal_splitter.addWidget(top_frame)
        horizontal_splitter.addWidget(self.text_edit)
        horizontal_splitter.setSizes([150, 400])

        # Create the second splitter (vertical)
        vertical_splitter = QSplitter(Qt.Orientation.Vertical)
        vertical_splitter.addWidget(bottom_frame)
        vertical_splitter.addWidget(horizontal_splitter)
        vertical_splitter.setSizes([50, 300])

        # Set layout
        layout = QHBoxLayout(self)
        layout.addWidget(vertical_splitter)
        self.setLayout(layout)
        self.setFixedSize(QSize(800, 480))


    def _create_frame(self, style: str) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet(style)
        return frame


    def _load_todos(self) -> None:
        # Load todos from the JSON file if it exists
        if os.path.exists(self._file_path):
            with open(self._file_path, 'r') as file:
                self._todos = json.load(file)
                # Populate the todo list in the UI
                for todo in self._todos:
                    self.todo_list.addItem(self._format_todo_preview(todo))


    def _save_todos(self) -> None:
        # Save the current todos to the JSON file
        with open(self._file_path, 'w') as file:
            json.dump(self._todos, file, indent=4)


    def _add_todo(self) -> None:
        # Prompt user to enter a new todo
        todo_text, ok = QInputDialog.getText(self, "New Todo", "Enter todo:")
        if ok and todo_text:
            self._todos.append(todo_text)
            self.todo_list.addItem(self._format_todo_preview(todo_text))

            # Automatically select the newly added item
            self.todo_list.setCurrentRow(self.todo_list.count() - 1)
            self._display_todo(self.todo_list.currentItem())

            # Save to file after adding a new todo
            self._save_todos()


    def _format_todo_preview(self, todo_text: str) -> str:
        # Return the first line or first 50 characters, whichever comes first
        first_line = todo_text.splitlines()[0]
        if len(first_line) > 50:
            return first_line[:50] + "..."
        return first_line


    def _display_todo(self, item) -> None:
        # Enable the text editor and display the selected todo
        self.text_edit.setDisabled(False)
        # Find the full text corresponding to the selected preview text
        full_text = self._todos[self.todo_list.row(item)]
        self.text_edit.setText(full_text)


    def _update_todo(self) -> None:
        # Update the selected todo with the edited text
        current_item = self.todo_list.currentItem()
        if current_item:
            updated_text = self.text_edit.toPlainText()
            self._todos[self.todo_list.row(current_item)] = updated_text
            current_item.setText(self._format_todo_preview(updated_text))

            # Save to file after modifying a todo
            self._save_todos()

