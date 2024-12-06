import sys

from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QFrame, QHBoxLayout, QPushButton, QMainWindow
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve


class FirstEnter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сторінка першого входу")
        self.setStyleSheet("background-color: #F7F2F2;")

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
        central_layout.setSpacing(10)

        # Заголовок (header)
        header = QFrame()
        header.setStyleSheet("background-color: #F7F2F2;")
        header.setFixedHeight(110)
        header_layout = QHBoxLayout(header)

        # Іконка
        self.hand_icon = QLabel()
        pixmap = QPixmap("images/financial.png").scaled(
            55, 55,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.hand_icon.setPixmap(pixmap)
        self.hand_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Текст у заголовку
        self.header_label = QLabel("Financial cost\nmanagement system")
        self.header_label.setStyleSheet("font-size: 26px; color: #000000; font-weight: bold;")

        header_layout.addWidget(self.hand_icon, alignment=Qt.AlignmentFlag.AlignLeft)
        header_layout.addWidget(self.header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Додати заголовок у центральний лейаут
        central_layout.addWidget(header)

        # Титульний текст
        title = QLabel("ЛАСКАВО ПРОСИМО ДО \nЗАСТОСУНКУ ДЛЯ УПРАВЛІННЯ \nФІНАНСОВИМИ ВИТРАТАМИ", self)
        central_layout.addWidget(title, alignment= Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 32px; 
                font-weight: bold; 
                color: #000000;
                padding: 5px;
                margin-top: 80px;
                text-align: center;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Додати колонки до основного лейауту
        main_layout.addLayout(left_column)
        main_layout.addLayout(central_layout)
        main_layout.addLayout(right_column)

        # Застосування основного лейауту
        self.setLayout(main_layout)

        # Додати кнопку реєстрації

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)  # Space between buttons
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align the buttons layout to the center

        # Add buttons to the horizontal layout
        button1 = create_custom_button("Зареєструватися", self, self.handle_registr)
        button2 = create_custom_button("Увійти", self, self.go_to_login_page)


        button_layout.addWidget(button1, alignment=Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(button2, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add the horizontal layout to the central layout
        central_layout.addLayout(button_layout)


        # Зберегти анімації як атрибути
        self.icon_animation = QPropertyAnimation(self.hand_icon, b"pos")
        self.text_animation = QPropertyAnimation(self.header_label, b"pos")
        self.start_animation()

    def anim(self, some, animation, w, h):
        some.move(w, 0)
        animation.setDuration(2000)
        animation.setStartValue(QPoint(w, 0))
        animation.setEndValue(QPoint(w, h))
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        animation.start()

    def start_animation(self):
        # Анімація для іконки
        self.anim(self.hand_icon, self.icon_animation, 310, 30)

        # Анімація для тексту
        self.anim(self.header_label, self.text_animation, 380, 35)

    def handle_registr(self):
        from registration import Registration
        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            main_page = Registration()  # Ініціалізуємо сторінку реєстрації
            main_window.setCentralWidget(main_page)  # Замінюємо центральний віджет
            self.deleteLater()

    def go_to_login_page(self):
        from select_user import SelectUser
        main_window = self.window()

        if isinstance(main_window, QMainWindow):

            select_user = SelectUser()
            main_window.setCentralWidget(select_user)
            self.deleteLater()

    # def go_to_entry_page(self):
    #     from main_page import DocumentCreationWindow
    #     main_window = self.window()
    #
    #     if isinstance(main_window, QMainWindow):
    #         main_page = DocumentCreationWindow()
    #         main_window.setCentralWidget(main_page)
    #         self.deleteLater()


def add_images_to_layout(layout, mirrored):
    layout.setSpacing(0)

    images = [
        "images/money.png",
        "images/bag.png",
        "images/wallet.png",
        "images/hand.png",
    ]

    for i in range(15):
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


def create_custom_button(text, parent, event):
    button = QPushButton(text, parent)
    button.setStyleSheet(""" 
                QPushButton {
                    background-color: #487EF1;
                    color: #000000;
                    font-size: 22px;
                    border-radius: 20px;
                    padding: 10px 20px;
                    border: 3px solid #000000; 
                }
                QPushButton:hover {
                    background-color: #0059b3;
                    border: 3px solid #000000;
                }
            """)
    button.setFixedSize(250, 55)
    button.clicked.connect(event)
    return button


if __name__ == '__main__':
    import main

    app = QApplication(sys.argv)
    window = main.MainApp()
    sys.exit(app.exec())
