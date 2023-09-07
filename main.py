import sys
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox, QMessageBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedSize(QSize(500, 500))

        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction(QIcon("icons/add.png"), "Add_Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)
        self.table.verticalHeader().setVisible(False)
        # Create toolbar and add elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create Status Bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a click
        self.table.cellClicked.connect(self.cellclicked)

    def cellclicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM STUDENTS")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        window = SearchDialog()
        window.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created during the Python Mega Course
        Feel free to review the code
        """
        self.setText(content)


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        self.setFixedSize(300, 100)

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1, )
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        index = student_app.table.currentRow()
        student_id = student_app.table.item(index, 0).text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM STUDENTS where id = ? ",
                       (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Success")
        confirmation.setText("Delete Successful")
        confirmation.exec()
        self.accept()
        # Refresh the table
        student_app.load_data()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedSize(300, 300)

        index = student_app.table.currentRow()
        student_name = student_app.table.item(index, 1).text()

        # Get ID for Selected row
        self.student_id = student_app.table.item(index, 0).text()
        layout = QVBoxLayout()
        # add student name widget
        self.student_name = QLineEdit(student_name)

        layout.addWidget(self.student_name)
        # add combo box for courses

        course_name = student_app.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Programming"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)
        # add mobile number

        mobile = student_app.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        layout.addWidget(self.mobile)

        # Add Submit Button
        submit = QPushButton("Submit")
        submit.clicked.connect(self.update_student)
        layout.addWidget(submit)
        self.setLayout(layout)

    def update_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE STUDENTS SET name = ?, course = ?, mobile = ? where id = ? ",
                       (name, course, mobile, self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Success")
        confirmation.setText("Update Successful")
        confirmation.exec()
        self.accept()
        # Refresh the table
        student_app.load_data()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()
        # add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        # add combo box for courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Programming"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        # add mobile number
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add Submit Button
        submit = QPushButton("Submit")
        submit.clicked.connect(self.add_student)
        layout.addWidget(submit)
        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO STUDENTS (name,course,mobile) VALUES (?,?,?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Success")
        confirmation.setText("Registration Successful")
        confirmation.exec()
        self.accept()
        student_app.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Students")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        layout.addWidget(self.search_bar)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)
        self.setLayout(layout)

    def search(self):
        name = self.search_bar.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM STUDENTS "
                                "WHERE NAME = ?", (name,))
        rows = list(result)
        items = student_app.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            student_app.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()
        self.accept()


app = QApplication(sys.argv)
student_app = MainWindow()
student_app.show()
student_app.load_data()
sys.exit(app.exec())
