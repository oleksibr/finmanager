from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt


class CreateDB(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Створення нової системи")
        self.setStyleSheet("background-color: #F7F2F2;")
        self.setFixedSize(800, 600)

        # Основний лейаут
        layout = QVBoxLayout()
        layout.setContentsMargins(150, 100, 150, 150)
        # Лейбл для інструкції
        message_label = QLabel("Введіть назву нової \nсистеми фінансових витрат:", self)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet("font-size: 20px; color: #000000; padding: 20px; font-weight: bold;")
        layout.addWidget(message_label)

        # Поле для введення назви БД
        self.db_name_input = QLineEdit(self)
        self.db_name_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                font-size: 16px;
                padding: 5px;
                color: #000;
                border: 2px solid #000000;
                border-radius: 20px;
                font-weight: bold;
            }
        """)
        self.db_name_input.setPlaceholderText("Назва системи фінансових витрат")
        self.db_name_input.setFixedSize(400, 40)
        layout.addWidget(self.db_name_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка для створення нової БД
        create_button = QPushButton("Створити", self)
        create_button.setStyleSheet(""" 
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
        create_button.setFixedSize(150, 50)
        layout.addWidget(create_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Підключаємо кнопку до функції створення БД
        create_button.clicked.connect(self.create_database)

        self.setLayout(layout)

    def create_database(self):
        db_name = self.db_name_input.text()
        if db_name:
            # Логіка створення бази даних
            try:
                # Припустимо, що ми використовуємо SQLite для створення БД
                import sqlite3
                conn = sqlite3.connect(f"{db_name}")
                conn.close()
                print(f"База даних '{db_name}' створена успішно.")
                self.close()  # Закриваємо вікно після успішного створення БД
            except Exception as e:
                print(f"Помилка при створенні БД: {e}")
        else:
            print("Будь ласка, введіть назву бази даних!")
