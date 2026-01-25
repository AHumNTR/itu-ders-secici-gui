from os.path import exists
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
class JsonForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JSON Form Filler")

        # --- Account ---
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        account_layout = QVBoxLayout()
        account_layout.addWidget(QLabel("Username:"))
        account_layout.addWidget(self.username_edit)
        account_layout.addWidget(QLabel("Password:"))
        account_layout.addWidget(self.password_edit)

        # --- Time ---
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

        # --- Courses ---
        self.crn_list = QListWidget()
        self.scrn_list = QListWidget()

        crn_buttons = QHBoxLayout()
        add_crn_btn = QPushButton("Add CRN")
        add_crn_btn.clicked.connect(lambda: self.add_item(self.crn_list))
        del_crn_btn = QPushButton("Remove CRN")
        del_crn_btn.clicked.connect(lambda: self.remove_item(self.crn_list))
        crn_buttons.addWidget(add_crn_btn)
        crn_buttons.addWidget(del_crn_btn)

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
        save_button = QPushButton("Save JSON")
        save_button.clicked.connect(self.save_json)

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Account"))
        main_layout.addLayout(account_layout)
        main_layout.addWidget(QLabel("Time"))
        main_layout.addLayout(time_layout)
        main_layout.addWidget(QLabel("Courses"))
        main_layout.addLayout(courses_layout)
        main_layout.addWidget(save_button)

        self.setLayout(main_layout)
        self.load_json()

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

        filename  = CONFIG_FILE_PATH
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Success", f"Saved to {filename}")
    def load_json(self):
        if(exists(CONFIG_FILE_PATH)==False):
            return
        data=json.load(open(CONFIG_FILE_PATH))
        print(data)
        self.username_edit.setText(data.get("account")["username"])
        self.password_edit.setText(data.get("account")["password"])
        self.year_spin.setValue(data.get("time")["year"])
        self.month_spin.setValue(data.get("time")["month"])
        self.day_spin.setValue(data.get("time")["day"])
        self.hour_spin.setValue(data.get("time")["hour"])
        self.minute_spin.setValue(data.get("time")["minute"])
        self.crn_list.addItems(data.get("courses")["crn"])
        self.scrn_list.addItems(data.get("courses")["scrn"])
        


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Itu Ders Zimbirtisi")

        # --- Account ---
        self.username = QLabel()
        self.password = QLabel()

        account_layout = QVBoxLayout()
        account_layout.addWidget(QLabel("Username:"))
        account_layout.addWidget(self.username)
        account_layout.addWidget(QLabel("Password:"))
        account_layout.addWidget(self.password)
        
        # --- Time ---
        self.year_spin = QLabel()

        self.month_spin = QLabel()

        self.day_spin = QLabel()

        self.hour_spin = QLabel()

        self.minute_spin = QLabel()

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

        # --- Courses ---
        self.crn_list = QListWidget()
        self.scrn_list = QListWidget()


        courses_layout = QVBoxLayout()
        courses_layout.addWidget(QLabel("CRN List:"))
        courses_layout.addWidget(self.crn_list)
        courses_layout.addWidget(QLabel("SCRN List:"))
        courses_layout.addWidget(self.scrn_list)

        # --- Save Button ---
        custom_layout=QVBoxLayout()
        editButton=QPushButton("Edit")
        editButton.pressed.connect(self.edit_data)
        startButton=QPushButton("Start")
        startButton.pressed.connect(self.start_ders_secici)
        self.output=QTextEdit()
        self.process=QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardOutput.connect(self.handle_stderr)
        custom_layout.addWidget(editButton)
        custom_layout.addWidget(self.output)
        custom_layout.addWidget(startButton)
        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Account"))
        main_layout.addLayout(account_layout)
        main_layout.addWidget(QLabel("Time"))
        main_layout.addLayout(time_layout)
        main_layout.addWidget(QLabel("Courses"))
        main_layout.addLayout(courses_layout)
        main_layout.addLayout(custom_layout)

        self.setLayout(main_layout)
        self.load_json()
    def start_ders_secici(self):
        self.output.append("starting itu-ders-secici")
        
        # Check if we are running as a frozen executable (PyInstaller)
        if getattr(sys, 'frozen', False):
            # Run "myself" (the exe) with the worker flag
            executable = sys.executable
            arguments = ["--worker"]
        else:
            # Run from source (python script)
            executable = sys.executable
            arguments = ["-u", "src/run.py"]
            
        self.process.start(executable, arguments)
    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output.append(data)

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.output.append(f"<span style='color:red;'>{data}</span>")

    def edit_data(self):
        jsonform=JsonForm()
        jsonform.show()
        
    def add_item(self, list_widget):
        text, ok = QInputDialog.getText(self, "Add Item", "Enter value:")
        if ok and text.strip():
            list_widget.addItem(text.strip())

    def remove_item(self, list_widget):
        for item in list_widget.selectedItems():
            list_widget.takeItem(list_widget.row(item))

    def load_json(self):
        if(exists(CONFIG_FILE_PATH)==False):
            return
        data=json.load(open(CONFIG_FILE_PATH))
        self.username.setText(data.get("account")["username"])
        self.password.setText(data.get("account")["password"])
        self.year_spin.setText(str(data.get("time")["year"]))
        self.month_spin.setText(str(data.get("time")["month"]))
        self.day_spin.setText(str(data.get("time")["day"]))
        self.hour_spin.setText(str(data.get("time")["hour"]))
        self.minute_spin.setText(str(data.get("time")["minute"]))
        self.crn_list.addItems(data.get("courses")["crn"])
        self.scrn_list.addItems(data.get("courses")["scrn"])
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
