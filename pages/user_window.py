from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit


class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Користувачі")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #F7F2F2;")

        # Основний макет
        self.layout = QVBoxLayout()

        # Лейбл для поточного користувача
        self.label = QLabel(f"Поточний користувач: ")
        self.label.setStyleSheet("font-size: 24px; color: #000000; font-weight: bold;")
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка для відкриття форми реєстрації
        new_user_btn = QPushButton("Додати користувача", self)
        new_user_btn.clicked.connect(self.show_registration_form)
        new_user_btn.setStyleSheet(""" 
                    QPushButton {
                        background-color: #B1C3FC;
                        border-radius: 20px;
                        font-size: 16px;
                        padding: 10px 20px;
                        color: #000000;
                        border: 2px solid #000000;
                        font-weight: bold;
                        }
                    QPushButton:hover {
                        background-color: #406CF6;
                        border: 2px solid #000000;
                        }
                    """)
        new_user_btn.setFixedSize(200, 50)
        self.layout.addWidget(new_user_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def show_registration_form(self):
        # Лейбл для поля логіну
        login_label = QLabel("Введіть логін:")
        login_label.setStyleSheet("font-size: 18px; color: #000000; font-weight: bold;")
        self.layout.addWidget(login_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.login_input = QLineEdit(self)
        self.login_input.setPlaceholderText("Логін")
        self.login_input.setStyleSheet("""
                    font-size: 16px;
                    padding: 5px;
                    background-color: #FFFFFF;
                    border: 2px solid #d3d3d3;
                    border-radius: 10px;
                    color: #000000;
                """)
        self.layout.addWidget(self.login_input)
        self.login_input.setFixedSize(300, 40)
        self.layout.addWidget(self.login_input, alignment=Qt.AlignmentFlag.AlignCenter)
        # Лейбл для поля паролю
        password_label = QLabel("Введіть пароль:")
        password_label.setStyleSheet("font-size: 18px; color: #000000; font-weight: bold;")
        self.layout.addWidget(password_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Поле вводу для паролю
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
                            font-size: 16px;
                            padding: 5px;
                            background-color: #FFFFFF;
                            border: 2px solid #d3d3d3;
                            border-radius: 10px;
                            color: #000000;
                        """)
        self.layout.addWidget(self.password_input)
        self.password_input.setFixedSize(300, 40)
        self.layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка для завершення реєстрації (можна додати функціональність)
        register_btn = QPushButton("Зареєструвати", self)
        register_btn.clicked.connect(self.register_user)
        register_btn.setStyleSheet(""" 
                    QPushButton {
                        background-color: #B1C3FC;
                        border-radius: 20px;
                        font-size: 16px;
                        padding: 10px 20px;
                        color: #000000;
                        border: 2px solid #000000;
                        font-weight: bold;
                        }
                    QPushButton:hover {
                        background-color: #406CF6;
                        border: 2px solid #000000;
                        }
                    """)
        register_btn.setFixedSize(230, 50)
        self.layout.addWidget(register_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def register_user(self):
        # Тут можна додати логіку реєстрації (наприклад, зберігати логін та пароль)
        login = self.login_input.text()
        password = self.password_input.text()
        print(f"Логін: {login}, Пароль: {password}")
