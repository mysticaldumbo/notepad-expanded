import sys
import json
import random
import string
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit, QListWidget, QDialog, QLineEdit, QAction, QMenu, QMessageBox, QColorDialog, QFontDialog, QFileDialog, QTextBrowser, QInputDialog, QCheckBox, QSlider, QComboBox
from PyQt5.QtCore import Qt

class Note:
    def __init__(self, title, content, locked=False):
        self.title = title
        self.content = content
        self.locked = locked

class NoteList:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def remove_note(self, index):
        del self.notes[index]

    def save_notes(self, filename):
        data = {"notes": [{"title": note.title, "content": note.content, "locked": note.locked} for note in self.notes]}
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_notes(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.notes = [Note(note['title'], note['content'], note.get('locked', False)) for note in data['notes']]

class AddNoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Note")
        layout = QVBoxLayout()
        self.title_label = QLabel("Title:")
        layout.addWidget(self.title_label)
        self.title_edit = QLineEdit()
        layout.addWidget(self.title_edit)
        self.content_label = QLabel("Content:")
        layout.addWidget(self.content_label)
        self.content_edit = QTextEdit()
        layout.addWidget(self.content_edit)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def get_note_info(self):
        return self.title_edit.text(), self.content_edit.toPlainText()

class ViewNoteDialog(QDialog):
    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout()

        self.title_label = QLabel("Title:")
        layout.addWidget(self.title_label)
        self.title_label = QLabel(title)
        layout.addWidget(self.title_label)

        self.content_label = QLabel("Content:")
        layout.addWidget(self.content_label)
        self.content_edit = QTextEdit()
        self.content_edit.setPlainText(content)
        self.content_edit.setReadOnly(True)
        layout.addWidget(self.content_edit)

        self.setLayout(layout)

class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ProdP - Your Production++ Notepad")
        self.note_list = NoteList()
        self.note_list.load_notes('notes.json')
        self.settings = self.load_settings()
        self.create_widgets()
        self.set_dark_mode()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings_data = json.load(f)
            return settings_data
        except FileNotFoundError:
            return {}

    def create_widgets(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.title_label = QLabel("ProdP - Your Production++ Notepad")
        self.layout.addWidget(self.title_label)

        self.note_listbox = QListWidget()
        self.note_listbox.itemDoubleClicked.connect(self.show_note_content)
        self.note_listbox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.note_listbox.customContextMenuRequested.connect(self.show_context_menu)
        self.update_note_listbox()
        self.layout.addWidget(self.note_listbox)

        self.add_note_button = QPushButton("Add Note")
        self.add_note_button.clicked.connect(self.add_note)
        self.layout.addWidget(self.add_note_button)

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.show_help)
        self.layout.addWidget(self.help_button)

        self.dev_mode_button = QPushButton("Developer Mode")
        self.dev_mode_button.clicked.connect(self.show_developer_mode)
        self.layout.addWidget(self.dev_mode_button)

        self.import_txt_button = QPushButton("Import .txt")
        self.import_txt_button.clicked.connect(self.import_txt)
        self.layout.addWidget(self.import_txt_button)

        self.open_calculator_button = QPushButton("Calculator")
        self.open_calculator_button.clicked.connect(self.open_calculator)
        self.layout.addWidget(self.open_calculator_button)

        self.central_widget.setLayout(self.layout)

    def add_note(self):
        dialog = AddNoteDialog(self)
        if dialog.exec_():
            title, content = dialog.get_note_info()
            if title and content:
                self.note_list.add_note(Note(title, content))
                self.update_note_listbox()
                self.note_list.save_notes('notes.json')

    def show_context_menu(self, pos):
        index = self.note_listbox.indexAt(pos)
        if index.isValid():
            context_menu = QMenu(self)
            view_action = QAction("View Note", self)
            view_action.triggered.connect(lambda: self.view_note(index))
            context_menu.addAction(view_action)
            note = self.note_list.notes[index.row()]
            if not note.locked:
                edit_action = QAction("Edit Note", self)
                edit_action.triggered.connect(lambda: self.edit_note(index))
                delete_action = QAction("Delete Note", self)
                delete_action.triggered.connect(lambda: self.delete_note(index))
                lock_action = QAction("Lock Note", self)
                lock_action.triggered.connect(lambda: self.lock_note(index))
                context_menu.addAction(edit_action)
                context_menu.addAction(delete_action)
                context_menu.addAction(lock_action)
            else:
                unlock_action = QAction("Unlock Note", self)
                unlock_action.triggered.connect(lambda: self.unlock_note(index))
                context_menu.addAction(unlock_action)
            save_as_txt_action = QAction("Save as .txt", self)
            save_as_txt_action.triggered.connect(lambda: self.save_as_txt(index))
            context_menu.addAction(save_as_txt_action)
            context_menu.exec_(self.note_listbox.mapToGlobal(pos))

    def view_note(self, index):
        note = self.note_list.notes[index.row()]
        if note.locked:
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            user_input, ok = QInputDialog.getText(self, "Unlock Note", f"Enter the 20 character string to unlock the note:\n{random_string}")
            if ok:
                if user_input == random_string:
                    dialog = ViewNoteDialog(note.title, note.content, self)
                    dialog.exec_()
                else:
                    QMessageBox.warning(self, "Incorrect String", "The string you entered is incorrect. Please try again.")
        else:
            dialog = ViewNoteDialog(note.title, note.content, self)
            dialog.exec_()

    def lock_note(self, index):
        note = self.note_list.notes[index.row()]
        if self.confirm_action("Confirm Lock", "Are you sure you want to lock this note?"):
            note.locked = True
            self.update_note_listbox()
            self.note_list.save_notes('notes.json')

    def unlock_note(self, index):
        note = self.note_list.notes[index.row()]
        if note.locked:
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            user_input, ok = QInputDialog.getText(self, "Unlock Note", f"Enter the 20 character string to unlock the note:\n{random_string}")
            if ok:
                if user_input == random_string:
                    note.locked = False
                    self.update_note_listbox()
                    self.note_list.save_notes('notes.json')
                else:
                    QMessageBox.warning(self, "Incorrect String", "The string you entered is incorrect. Please try again.")
        else:
            QMessageBox.warning(self, "Note Unlocked", "This note is already unlocked.")

        def save_as_txt(self, index):
            note = self.note_list.notes[index.row()]
            filename, _ = QFileDialog.getSaveFileName(self, "Save as .txt", f"{note.title}.txt", "Text Files (*.txt)")
            if filename:
                with open(filename, 'w') as f:
                    f.write(note.content)

    def set_dark_mode(self):
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #2c2c2c, stop:1 black); color: yellow;")


    def show_help(self):
        message = QMessageBox()
        message.setWindowTitle("Help")
        message.setText("ProdP - Your Production++ Notepad\n\nFeatures:\n\n- Add Note: Click this button to add a new note.\n\n- Right Clicks - Select a note then right-click it to View Edit, Delete, Save as, Lock, or Unlock it.\n\n- Developer Mode: Open the Python executor/terminal (ExecutePy.py).\n\n- Import .txt: Import a .txt file into Notelist.\n\n- Calculator: Open a calculator. What did you expect?\n\n- Ignore: if you view a file named ignore you can't view it, though you can still do the rest of the options.\n\n- Help: Click this button to display this help message.")
        message.setStyleSheet("background-color: black; color: yellow;")
        message.exec_()

    def confirm_action(self, title, message):
        confirm_dialog = QMessageBox()
        confirm_dialog.setWindowTitle(title)
        confirm_dialog.setText(message)
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_dialog.setDefaultButton(QMessageBox.No)
        return confirm_dialog.exec_() == QMessageBox.Yes
    
    def show_note_content(self, item):
        index = self.note_listbox.row(item)
        note = self.note_list.notes[index]
        dialog = ViewNoteDialog(note.title, note.content, self)
        dialog.exec_()

    def update_note_listbox(self):
        self.note_listbox.clear()
        for note in self.note_list.notes:
            self.note_listbox.addItem(note.title)

    def delete_note(self, index):
        if self.settings.get('disable_confirmation', False) or self.confirm_action("Confirm Delete", "Are you sure you want to delete this note?"):
            self.note_list.remove_note(index.row())
            self.update_note_listbox()
            self.note_list.save_notes('notes.json')

    def save_as_txt(self, index):
        note = self.note_list.notes[index.row()]
        filename, _ = QFileDialog.getSaveFileName(self, "Save as .txt", f"{note.title}.txt", "Text Files (*.txt)")
        if filename:
            with open(filename, 'w') as f:
                f.write(note.content)

    def view_note(self, index):
        note = self.note_list.notes[index.row()]
        if note.title == "ignore":
            pass
        else:
            dialog = ViewNoteDialog(note.title, note.content, self)
            dialog.exec_()

    def show_developer_mode(self):
        os.system("python ExecutePy.py")

    def open_calculator(self):
        os.system("python calculator.py")

    def import_txt(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Import .txt", filter="Text Files (*.txt)")
        if filename:
            with open(filename, 'r') as f:
                content = f.read()
            title, ok = QInputDialog.getText(self, "Enter Note Title", "Enter a title for the note:")
            if ok:
                self.note_list.add_note(Note(title, content))
                self.update_note_listbox()
                self.note_list.save_notes('notes.json')
    def edit_note(self, index):
        note = self.note_list.notes[index.row()]
        dialog = AddNoteDialog(self)
        dialog.setWindowTitle("Edit Note")
        dialog.title_edit.setText(note.title)
        dialog.content_edit.setPlainText(note.content)

        if dialog.exec_():
            title, content = dialog.get_note_info()
            if title and content:
                note.title = title
                note.content = content
                self.update_note_listbox()
                self.note_list.save_notes('notes.json')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec_())