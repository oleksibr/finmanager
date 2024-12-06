from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QDialog
from PyQt6.QtCore import Qt
import finmanager.models.utils_db as util
import finmanager.models.models as model

# class CreateDB(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.result_value = None  # Для збереження значення, яке потрібно повернути
#
#
#         # Основний лейаут
#         layout = QVBoxLayout()
#         layout.setContentsMargins(150, 100, 150, 150)
#         # Лейбл для інструкції
#         message_label = QLabel("Введіть назву нової \nсистеми фінансових витрат:", self)
#         message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         message_label.setStyleSheet("font-size: 20px; color: #000000; padding: 20px; font-weight: bold;")
#         layout.addWidget(message_label)
#
#         # Поле для введення назви БД
#         self.input = QLineEdit(self)
#         self.input.setStyleSheet("""
#             QLineEdit {
#                 background-color: #FFFFFF;
#                 font-size: 16px;
#                 padding: 5px;
#                 color: #000;
#                 border: 2px solid #000000;
#                 border-radius: 20px;
#                 font-weight: bold;
#             }
#         """)
#         self.input.setPlaceholderText("Назва системи фінансових витрат")
#         self.input.setFixedSize(400, 40)
#         layout.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         #button_layout = QHBoxLayout()
#         # Кнопка для створення нової БД
#         create_button = QPushButton("Створити", self)
#         create_button.setStyleSheet("""
#             QPushButton {
#                       background-color: #B1C3FC;
#                       color: #000000;
#                       font-size: 18px;
#                       border-radius: 20px;
#                       padding: 10px 20px;
#                       border: 3px solid #000000;
#                       font-weight: bold;
#                   }
#                   QPushButton:hover {
#                       background-color: #406CF6;
#                       border: 3px solid #FFFFFF;
#                   }
#               """)
#         create_button.setFixedSize(150, 50)
#         layout.addWidget(create_button, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         # Підключаємо кнопку до функції створення БД
#         create_button.clicked.connect(self.create_database)
#
#         cancel_button = QPushButton("Скасувати", self)
#         cancel_button.setStyleSheet("""
#             QPushButton {
#                       background-color: #B1C3FC;
#                       color: #000000;
#                       font-size: 18px;
#                       border-radius: 20px;
#                       padding: 10px 20px;
#                       border: 3px solid #000000;
#                       font-weight: bold;
#                   }
#                   QPushButton:hover {
#                       background-color: #406CF6;
#                       border: 3px solid #FFFFFF;
#                   }
#               """)
#         cancel_button.setFixedSize(150, 50)
#         layout.addWidget(cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         # Підключаємо кнопку до функції створення БД
#         cancel_button.clicked.connect(self.cancel_new_database)
#
#         #self.setLayout(button_layout)
#
#         self.setLayout(layout)
#
#     def create_database(self):
#         if not self.input.text():
#             return 2
#         util.create_default_db(self.input.text())
#         return 1
#
#     def cancel_new_database(self):
#         self.close()
#
class CreateDB(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.result_value = None  # Для збереження значення, яке потрібно повернути
        self.setStyleSheet("background-color: #F7F2F2;")
        # Основний лейаут
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        self.setFixedSize(600, 300)

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

        # Горизонтальний макет для кнопок
        button_layout = QHBoxLayout()

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
        create_button.clicked.connect(self.create_database)
        button_layout.addWidget(create_button)

        # Кнопка для скасування
        cancel_button = QPushButton("Скасувати", self)
        cancel_button.setStyleSheet(""" 
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
        cancel_button.setFixedSize(150, 50)
        cancel_button.clicked.connect(self.cancel_new_database)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def create_database(self):
        db_name = self.db_name_input.text().strip()
        if not db_name:
            self.result_value = 2  # Повертаємо код помилки
        else:
            util.create_default_db(db_name)  # Ваш метод для створення БД
            self.result_value = 1  # Успішно
        self.accept()  # Закриваємо діалог з поверненням результату

    def cancel_new_database(self):
        self.result_value = None  # Повертаємо None
        self.reject()  # Закриваємо діалог без результату
