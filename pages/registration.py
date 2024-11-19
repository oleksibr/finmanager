import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QTransform


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
        self.add_images_to_layout(left_column, mirrored=False)

        # Права колонка із зображеннями
        right_column = QVBoxLayout()
        self.add_images_to_layout(right_column, mirrored=True)

        # Центральна частина
        central_layout = QVBoxLayout()
        central_layout.setSpacing(15)  # Скоротити відстань між елементами
        central_layout.setContentsMargins(20, 20, 20, 20)  # Зменшити відступи з боків

        # Заголовок
        title = QLabel("РЕЄСТРАЦІЯ", self)
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #000000; margin-top: 10px;")
        central_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Поля вводу
        self.add_input_field(central_layout, "Введіть логін:", "Логін")
        self.add_input_field(central_layout, "Введіть пароль:", "Пароль", echo_mode=True)
        self.add_input_field(central_layout, "Підтвердьте пароль:", "Пароль", echo_mode=True)

        # Кнопка для завершення реєстрації
        register_btn = QPushButton("Зареєструвати користувача", self)
        register_btn.clicked.connect(self.register_user)
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #B1C3FC;
                border-radius: 20px;
                font-size: 20px;
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
        register_btn.setFixedSize(320, 50)
        central_layout.addWidget(register_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Додати центральний лейаут в основний лейаут
        main_layout.addLayout(left_column)
        main_layout.addLayout(central_layout)
        main_layout.addLayout(right_column)

        self.setLayout(main_layout)

    def add_input_field(self, layout, label_text, placeholder_text, echo_mode=False):
        """Додає пару лейбл + поле вводу до лейауту."""
        label = QLabel(label_text)
        label.setStyleSheet("font-size: 20px; color: #000000; font-weight: bold;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

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
        """)
        input_field.setFixedSize(500, 45)
        layout.addWidget(input_field, alignment=Qt.AlignmentFlag.AlignCenter)

        # Зберігаємо поле як атрибут для обробки
        if placeholder_text == "Логін":
            self.login_input = input_field
        elif placeholder_text == "Пароль" and not hasattr(self, "password_input"):
            self.password_input = input_field
        elif placeholder_text == "Пароль":
            self.password_confirm_input = input_field

    def add_images_to_layout(self, layout, mirrored):
        layout.setSpacing(0)

        images = [
            "images/money.png",
            "images/bag.png",
            "images/wallet.png",
            "images/hand.png",
        ]

        for i in range(9):
            image_label = QLabel()
            pixmap = QPixmap(images[i % len(images)])
            if mirrored:
                transform = QTransform().scale(-1, 1)  # Дзеркалення зображення
                pixmap = pixmap.transformed(transform)

            # Налаштування розміру зображення
            image_label.setPixmap(pixmap.scaled(
                40, 40,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

            # Контейнер для вирівнювання
            container = QWidget()
            container.setFixedSize(300, 60)  # Фіксований розмір області з картинкою
            container_layout = QHBoxLayout(container)
            container_layout.setContentsMargins(0, 10, 0, 10)  # Налаштування відступів
            container_layout.setSpacing(0)

            if i % 3 == 0:  # Вирівнювання ліворуч
                container_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignLeft)
            elif i % 3 == 1:  # Вирівнювання праворуч
                container_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignRight)
            else:  # Вирівнювання по центру
                container_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

            # Додавання контейнера до основного лейауту
            layout.addWidget(container)

    def register_user(self):
        """Перевірка введених даних при реєстрації."""
        login = self.login_input.text()
        password = self.password_input.text()
        confirm_password = self.password_confirm_input.text()
        if password == confirm_password:
            print(f"Користувача {login} успішно зареєстровано!")
        else:
            print("Паролі не співпадають!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Registration()
    window.show()
    sys.exit(app.exec())
