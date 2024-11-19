from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt


class DeleteDB(QWidget):
    def __init__(self, selected_db=""):
        super().__init__()

        self.setWindowTitle("Видалення системи")
        self.setStyleSheet("background-color: #F7F2F2;")
        self.setFixedSize(800, 600)

        # Основний лейаут
        layout = QVBoxLayout()
        layout.setContentsMargins(150, 150, 150, 150)
        # Лейбл з повідомленням
        message_label = QLabel("Ви справді хочете видалити \n цю систему фінансових витрат?", self)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet("font-size: 22px; color: #000000; padding: 20px; font-weight: bold;")
        layout.addWidget(message_label)
        layout.addSpacing(20)

        selected_db_label = QLabel("Обрана система:", self)
        selected_db_label.setStyleSheet("font-size: 20px; color: #000000; font-weight: bold;")
        layout.addWidget(selected_db_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(5)
        # Відображення назви обраної БД з меншою відстанню до підпису
        self.selected_db_display = QLabel(selected_db, self)
        self.selected_db_display.setStyleSheet("""
                    QLabel {
                        font-size: 18px; 
                        color: #000000; 
                        background-color: #FFFFFF; 
                        padding: 5px 10px;
                        border: 2px solid #000000;
                        border-radius: 20px;
                        font-weight: bold;
                    }
                """)
        self.selected_db_display.setFixedSize(300, 40)
        layout.addWidget(self.selected_db_display, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        # Кнопка "Так"
        delete_button = QPushButton("Так", self)
        delete_button.setStyleSheet(""" 
            QPushButton {
                      background-color: #B1C3FC;
                      color: #000000;
                      font-size: 18px;
                      border-radius: 20px;
                      padding: 10px 20px;
                      border: 3px solid #000000;
                      font-weight: bold;
                  }
                  QPushButton:hover {
                      background-color: #406CF6;
                      border: 3px solid #FFFFFF;
                  }
              """)
        delete_button.setFixedSize(150, 50)
        delete_button.clicked.connect(self.confirm_deletion)  # Додаємо обробник
        layout.addWidget(delete_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def confirm_deletion(self):
        # Створення діалогового вікна
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Підтвердження")
        msg_box.setText("Ви впевнені, що хочете видалити базу даних?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #F7F2F2;
                font-size: 16px;
            }
            QMessageBox QLabel {
                color: #000000;
            }
            QMessageBox QPushButton {
                background-color: #B1C3FC;
                border: 2px solid #000000;
                border-radius: 5px;
                padding: 5px 10px;
                color: #000000;
            }
            QMessageBox QPushButton:hover {
                background-color: #406CF6;
                color: #FFFFFF;
            }
        """)

        reply = msg_box.exec()

        if reply == QMessageBox.StandardButton.Yes:
            print("База даних успішно видалена!")  # Замініть на реальну логіку видалення
            self.close()  # Закриває тільки поточне вікно
        else:
            print("Видалення скасовано")