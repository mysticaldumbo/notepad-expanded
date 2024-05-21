import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QAction, QVBoxLayout, QWidget, QPlainTextEdit, QPushButton, QMessageBox, QMenu, QInputDialog
from PyQt5.QtGui import QCursor, QKeySequence
import webbrowser
import pyperclip

class OutputTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        pass

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = QTextEdit()
        self.output_edit = OutputTextEdit()
        self.clear_terminal_button = QPushButton('Clear Terminal')
        self.clear_terminal_button.clicked.connect(self.clear_terminal)
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.text_edit)
        self.central_layout.addWidget(self.output_edit)
        self.central_layout.addWidget(self.clear_terminal_button)

        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)

        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)

        save_as_action = QAction('Save As', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_as_file)

        run_menu = QMenu('Run', self)
        run_code_action = QAction('Run Code', self)
        run_code_action.setShortcut('Ctrl+R')
        run_code_action.triggered.connect(self.run_code)
        run_menu.addAction(run_code_action)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)

        menubar.addMenu(run_menu)

        menubar.addMenu(self.create_resources_menu())

        self.setWindowTitle('Text Editor')
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QTextEdit, QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                selection-background-color: #264f78;
                selection-color: #ffffff;
            }
            QPushButton {
                background-color: #264f78;
                color: #ffffff;
                border: 1px solid #264f78;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #1e1e1e;
                border: 1px solid #ffffff;
            }
            QMenuBar {
                background-color: #2d2d30;
            }
            QMenuBar::item {
                background-color: #2d2d30;
                color: #d4d4d4;
            }
            QMenuBar::item:selected {
                background-color: #264f78;
            }
            QMenu {
                background-color: #2d2d30;
                border: 1px solid #1e1e1e;
            }
            QMenu::item {
                background-color: #2d2d30;
                color: #d4d4d4;
            }
            QMenu::item:selected {
                background-color: #264f78;
            }
            """)

    def new_file(self):
        self.text_edit.clear()
        self.setWindowTitle('Text Editor')

    def open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open File')
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_edit.setPlainText(content)
                self.setWindowTitle(f'Text Editor - {file_path}')

    def save_file(self):
        if not hasattr(self, 'current_file_path') or not self.current_file_path:
            self.save_as_file()
        else:
            with open(self.current_file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())
                self.setWindowTitle(f'Text Editor - {self.current_file_path}')

    def save_as_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Save File')
        if file_path:
            self.current_file_path = file_path
            self.save_file()

    def clear_terminal(self):
        self.output_edit.clear()

    def create_resources_menu(self):
        resources_menu = QMenu('Resources', self)
        python_docs_action = QAction('Python Docs', self)
        python_docs_action.triggered.connect(lambda: self.open_python_docs())
        resources_menu.addAction(python_docs_action)
        create_rgb_action = QAction('Create RGB', self)
        create_rgb_action.setShortcut('Ctrl+M')  
        create_rgb_action.triggered.connect(lambda: self.open_rgb_maker())
        resources_menu.addAction(create_rgb_action)
        calculator_action = QAction('Calculator', self)
        calculator_action.setShortcut('Ctrl+Shift+C') 
        calculator_action.triggered.connect(lambda: self.open_calculator())
        resources_menu.addAction(calculator_action)
        return resources_menu

    def open_python_docs(self):
        webbrowser.open('https://docs.python.org/3/reference/index.html')

    def open_rgb_maker(self):
        subprocess.Popen(['python', 'rgbMaker.py'])

    def open_calculator(self):
        subprocess.Popen(['calc'])

    def run_code(self):
        code = self.text_edit.toPlainText()
        try:
            result = subprocess.check_output(['python', '-c', code], stderr=subprocess.STDOUT, text=True)
            self.output_edit.appendPlainText(result)
        except subprocess.CalledProcessError as e:
            self.output_edit.appendPlainText(f"Error: {e.output}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())