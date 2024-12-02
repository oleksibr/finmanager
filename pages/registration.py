import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QMainWindow
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from PyQt6.QtGui import QPixmap, QTransform

from first_enter import FirstEnter, add_images_to_layout, create_custom_button


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Реєстрація")
        self.setStyleSheet("background-color: #F7F2F2;")
        self.showMaximized()

        # Основний горизонтальний лейаут
        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)

        # Ліва колонка із зображеннями
        left_column = QVBoxLayout()
        add_images_to_layout(left_column, mirrored=False)

        # Права колонка із зображеннями
        right_column = QVBoxLayout()
        add_images_to_layout(right_column, mirrored=True)

        # Центральна частина
        central_layout = QVBoxLayout()
        central_layout.setSpacing(5)  # Зменшення відстані між елементами

        # Заголовок
        title = QLabel("РЕЄСТРАЦІЯ", self)
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #000000; margin-top: 50px;")
        central_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)

        input_field = QVBoxLayout()
        input_field.setSpacing(5)  # Зменшення відстані між полями вводу
        input_field.setContentsMargins(0, 0, 0, 0)  # Відсутність зайвих відступів
        # Поля вводу
        self.add_input_field(input_field, "Введіть логін:", "Логін")
        self.add_input_field(input_field, "Введіть пароль:", "Пароль", echo_mode=True)
        self.add_input_field(input_field, "Підтвердьте пароль:", "Пароль", echo_mode=True)

        input_field.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        central_layout.addLayout(input_field)

        # Кнопки
        button_layout = QVBoxLayout()
        button_layout.setSpacing(5)  # Space between buttons
        button_layout.setContentsMargins(0, 0, 0, 0)  # Відсутність додаткових відступів
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        button1 = create_custom_button("Зареєструватися", self, self.register_user)
        button2 = create_custom_button("Повернутися", self, self.go_to_first_page)
        button1.setFixedSize(250, 50)
        button2.setFixedSize(250, 50)
        button_layout.addWidget(button1, alignment=Qt.AlignmentFlag.AlignRight)
        button_layout.addWidget(button2, alignment=Qt.AlignmentFlag.AlignLeft)

        central_layout.addLayout(button_layout)

        # Додати центральний лейаут в основний лейаут
        main_layout.addLayout(left_column)
        main_layout.addLayout(central_layout)
        main_layout.addLayout(right_column)

        self.setLayout(main_layout)

    def add_input_field(self, layout, label_text, placeholder_text, echo_mode=False):
        """Додає пару лейбл + поле вводу до лейауту."""
        field_layout = QVBoxLayout()
        field_layout.setSpacing(3)  # Відстань між лейблом і полем вводу
        field_layout.setContentsMargins(0, 0, 0, 0)  # Вимкнення внутрішніх відступів

        label = QLabel(label_text)
        label.setStyleSheet("font-size: 20px; color: #000000; font-weight: bold; margin: 0;")
        field_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)

        input_field = QLineEdit(self)
        input_field.setPlaceholderText(placeholder_text)
        input_field.setEchoMode(QLineEdit.EchoMode.Password if echo_mode else QLineEdit.EchoMode.Normal)
        input_field.setStyleSheet("""
               font-size: 18px;
               padding: 5px;
               background-color: #FFFFFF;
               border: 2px solid #d3d3d3;
               border-radius: 10px;
               color: #000000;
               margin: 0;
           """)
        input_field.setFixedSize(500, 40)
        field_layout.addWidget(input_field, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addLayout(field_layout)

        if placeholder_text == "Логін":
            self.login_input = input_field
        elif placeholder_text == "Пароль" and not hasattr(self, "password_input"):
            self.password_input = input_field
        elif placeholder_text == "Повторення паролю":
            self.password_confirm_input = input_field

    def register_user(self):
        """Перевірка введених даних при реєстрації."""
        login = self.login_input.text()
        password = self.password_input.text()
        confirm_password = self.password_confirm_input.text()
        if password == confirm_password:
            print(f"Користувача {login} успішно зареєстровано!")
        else:
            print("Паролі не співпадають!")

    def go_to_first_page(self):
        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            first_enter = FirstEnter()  # Ініціалізуємо сторінку реєстрації
            main_window.setCentralWidget(first_enter)  # Замінюємо центральний віджет
            self.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Registration()
    window.show()
    sys.exit(app.exec())
