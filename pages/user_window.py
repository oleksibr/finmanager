from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QMainWindow


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
        new_user_btn.clicked.connect(self.handle_registr)
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
        new_user_btn.setFixedSize(230, 50)
        self.layout.addWidget(new_user_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def handle_registr(self):
        from registration import Registration
        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            main_page = Registration()  # Ініціалізуємо сторінку реєстрації
            main_window.setCentralWidget(main_page)  # Замінюємо центральний віджет
            self.deleteLater()


    def register_user(self):
        # Тут можна додати логіку реєстрації (наприклад, зберігати логін та пароль)
        login = self.login_input.text()
        password = self.password_input.text()
        print(f"Логін: {login}, Пароль: {password}")
