from ntpath import dirname
from os.path import exists
import os
import sys
import json
import run
from PyQt6.QtGui import QTextBlock
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QWidget, QLabel, QLineEdit, QSpinBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QListWidget, QInputDialog, QMessageBox, QFileDialog
)
from PyQt6.QtCore import QProcess

CONFIG_FILE_PATH = "data/config.json"

sys.stdout.reconfigure(line_buffering=True)
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Itu Ders Zimbirtisi")
        self.resize(500, 700) # Set a reasonable default size

        # --- Account Section ---
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        account_layout = QVBoxLayout()
        account_layout.addWidget(QLabel("Username:"))
        account_layout.addWidget(self.username_edit)
        account_layout.addWidget(QLabel("Password:"))
        account_layout.addWidget(self.password_edit)

        # --- Time Section ---
        self.year_spin = QSpinBox()
        self.year_spin.setRange(1900, 2100)
        self.year_spin.setValue(2025)

        self.month_spin = QSpinBox()
        self.month_spin.setRange(1, 12)

        self.day_spin = QSpinBox()
        self.day_spin.setRange(1, 31)

        self.hour_spin = QSpinBox()
        self.hour_spin.setRange(0, 23)

        self.minute_spin = QSpinBox()
        self.minute_spin.setRange(0, 59)

        time_layout = QVBoxLayout()
        for label, widget in [
            ("Year:", self.year_spin),
            ("Month:", self.month_spin),
            ("Day:", self.day_spin),
            ("Hour:", self.hour_spin),
            ("Minute:", self.minute_spin),
        ]:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            row.addWidget(widget)
            time_layout.addLayout(row)

        # --- Courses Section ---
        self.crn_list = QListWidget()
        self.scrn_list = QListWidget()

        # CRN Buttons
        crn_buttons = QHBoxLayout()
        add_crn_btn = QPushButton("Add CRN")
        add_crn_btn.clicked.connect(lambda: self.add_item(self.crn_list))
        del_crn_btn = QPushButton("Remove CRN")
        del_crn_btn.clicked.connect(lambda: self.remove_item(self.crn_list))
        crn_buttons.addWidget(add_crn_btn)
        crn_buttons.addWidget(del_crn_btn)

        # SCRN Buttons
        scrn_buttons = QHBoxLayout()
        add_scrn_btn = QPushButton("Add SCRN")
        add_scrn_btn.clicked.connect(lambda: self.add_item(self.scrn_list))
        del_scrn_btn = QPushButton("Remove SCRN")
        del_scrn_btn.clicked.connect(lambda: self.remove_item(self.scrn_list))
        scrn_buttons.addWidget(add_scrn_btn)
        scrn_buttons.addWidget(del_scrn_btn)

        courses_layout = QVBoxLayout()
        courses_layout.addWidget(QLabel("CRN List:"))
        courses_layout.addWidget(self.crn_list)
        courses_layout.addLayout(crn_buttons)
        courses_layout.addWidget(QLabel("SCRN List:"))
        courses_layout.addWidget(self.scrn_list)
        courses_layout.addLayout(scrn_buttons)

        # --- Save Button ---
        save_button = QPushButton("Save Config")
        save_button.clicked.connect(self.save_json)

        # --- Process / Execution Section ---
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        
        start_button = QPushButton("Start Script")
        start_button.clicked.connect(self.start_ders_secici)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardOutput.connect(self.handle_stderr)

        # --- Main Layout Assembly ---
        main_layout = QVBoxLayout()
        
        # Add sections
        main_layout.addWidget(QLabel("<b>Account</b>"))
        main_layout.addLayout(account_layout)
        
        main_layout.addWidget(QLabel("<b>Time</b>"))
        main_layout.addLayout(time_layout)
        
        main_layout.addWidget(QLabel("<b>Courses</b>"))
        main_layout.addLayout(courses_layout)
        
        main_layout.addWidget(save_button)
        main_layout.addWidget(QLabel("<b>Output Log</b>"))
        main_layout.addWidget(self.output)
        main_layout.addWidget(start_button)

        self.setLayout(main_layout)
        
        # Load initial data
        self.load_json()

    # --- Helper Methods (Moved from JsonForm) ---
    def add_item(self, list_widget):
        text, ok = QInputDialog.getText(self, "Add Item", "Enter value:")
        if ok and text.strip():
            list_widget.addItem(text.strip())

    def remove_item(self, list_widget):
        for item in list_widget.selectedItems():
            list_widget.takeItem(list_widget.row(item))

    def save_json(self):
        data = {
            "account": {
                "username": self.username_edit.text(),
                "password": self.password_edit.text(),
            },
            "time": {
                "year": self.year_spin.value(),
                "month": self.month_spin.value(),
                "day": self.day_spin.value(),
                "hour": self.hour_spin.value(),
                "minute": self.minute_spin.value(),
            },
            "courses": {
                "crn": [self.crn_list.item(i).text() for i in range(self.crn_list.count())],
                "scrn": [self.scrn_list.item(i).text() for i in range(self.scrn_list.count())],
            },
        }

        filename = CONFIG_FILE_PATH
        if filename:
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
                
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Success", f"Saved to {filename}")

    def load_json(self):
        if not exists(CONFIG_FILE_PATH):
            return
        
        try:
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Use .get with empty dict fallbacks to prevent crashes on partial configs
            account = data.get("account", {})
            time_data = data.get("time", {})
            courses = data.get("courses", {})

            self.username_edit.setText(account.get("username", ""))
            self.password_edit.setText(account.get("password", ""))
            
            self.year_spin.setValue(time_data.get("year", 2025))
            self.month_spin.setValue(time_data.get("month", 1))
            self.day_spin.setValue(time_data.get("day", 1))
            self.hour_spin.setValue(time_data.get("hour", 0))
            self.minute_spin.setValue(time_data.get("minute", 0))
            
            self.crn_list.clear()
            self.crn_list.addItems(courses.get("crn", []))
            
            self.scrn_list.clear()
            self.scrn_list.addItems(courses.get("scrn", []))
            
        except Exception as e:
            self.output.append(f"<span style='color:red;'>Error loading config: {e}</span>")

    # --- Process Methods ---
    def start_ders_secici(self):
        self.output.append("starting itu-ders-secici...")
        self.save_json()
        
        # Check if we are running as a frozen executable (PyInstaller)
        if getattr(sys, 'frozen', False):
            executable = sys.executable
            arguments = ["--worker"]
        else:
            executable = sys.executable
            arguments = ["-u", "src/run.py"]
            
        self.process.start(executable, arguments)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output.append(data)

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output.append(f"<span style='color:red;'>{data}</span>")
if __name__ == "__main__":
    if "--worker" in sys.argv:
        # PyInstaller --noconsole prevents stdout working by default. 
        # We must restore it to pipe output back to the GUI.
        if sys.stdout is None:
            sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)
        if sys.stderr is None:
            sys.stderr = open(2, 'w', encoding='utf-8', closefd=False)
            
        # Remove the flag so argparse in run.py doesn't crash
        sys.argv.remove("--worker")
        
        # Run the logic
        run.main()
        sys.exit(0)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
