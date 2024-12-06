from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QMessageBox, QMainWindow, QApplication)

import sys
from Utils import add_images_to_layout
from finmanager.pages.first_enter import FirstEnter
from first_enter import add_images_to_layout, create_custom_button


class SelectUser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Підтвердження користувача")
        self.setStyleSheet("background-color: #F7F2F2;")

        main_layout = QHBoxLayout()
        main_layout.setSpacing(100)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрування всіх елементів

        # Left column layout for images
        left_column = QVBoxLayout()
        add_images_to_layout(left_column, mirrored=False)  # Define this method to add images

        # Right column layout for images
        right_column = QVBoxLayout()
        add_images_to_layout(right_column, mirrored=True)  # Define this method to add images

        # Central layout for buttons and database selection
        central_layout = QVBoxLayout()
        central_layout.setSpacing(10)

        # Заголовок
        title = QLabel("ПІДТВЕРДТЬТЕ КОРИСТУВАЧА", self)
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #000000; padding: 20px;")
        central_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Поле для введення логіну
        login_label = QLabel("          Введіть логін:", self)
        login_label.setStyleSheet("font-size: 20px; color: #000000; margin-top: 10px;font-weight: bold;")
        central_layout.addWidget(login_label)

        login_input = QLineEdit(self)
        login_input.setPlaceholderText("Логін")
        login_input.setFixedSize(500, 40)
        login_input.setStyleSheet("""
            font-size: 20px;
            padding: 5px;
            background-color: #FFFFFF;
            border: 2px solid #d3d3d3;
            border-radius: 20px;
            color: #000000;
        """)
        central_layout.addWidget(login_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Поле для введення паролю
        password_label = QLabel("           Введіть пароль:", self)
        password_label.setStyleSheet("font-size: 20px; color: #000000; margin-top: 10px; font-weight: bold;")
        central_layout.addWidget(password_label)

        password_input = QLineEdit(self)
        password_input.setPlaceholderText("Пароль")
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_input.setFixedSize(500, 40)
        password_input.setStyleSheet("""
            font-size: 20px;
            padding: 5px;
            background-color: #FFFFFF;
            border: 2px solid #d3d3d3;
            border-radius: 20px;
            color: #000000;
        """)
        central_layout.addWidget(password_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Кнопки в одному горизонтальному розташуванні
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)  # Відстань між кнопками
        button_layout.addSpacerItem(QSpacerItem(15, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


        cancel_button = create_custom_button("Повернутися", self, self.go_to_first_page)
        cancel_button.setFixedSize(200, 50)
        button_layout.addWidget(cancel_button)

        ok_button = create_custom_button("OK", self, self.go_to_entry_page)
        ok_button.setFixedSize(200, 50)
        button_layout.addWidget(ok_button)

        central_layout.addLayout(button_layout)

        # Додаємо відступи зверху та знизу для центрованого розташування
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        central_layout.insertSpacerItem(0, spacer_top)
        central_layout.addSpacerItem(spacer_bottom)

        main_layout.addLayout(left_column)
        main_layout.addLayout(central_layout)
        main_layout.addLayout(right_column)

        self.setLayout(main_layout)

    def go_to_main_page(self):
        from entry_page import EntryPage
        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            main_page = EntryPage()
            main_window.setCentralWidget(main_page)
            self.deleteLater()

    def go_to_entry_page(self):
        from entry_page import EntryPage
        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            entry_page = EntryPage()
            main_window.setCentralWidget(entry_page)
            self.deleteLater()

    def go_to_first_page(self):
        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            first_enter = FirstEnter()  # Ініціалізуємо сторінку реєстрації
            main_window.setCentralWidget(first_enter)  # Замінюємо центральний віджет
            self.deleteLater()


if __name__ == '__main__':
    import main
    app = QApplication(sys.argv)
    window = main.MainApp()
    sys.exit(app.exec())