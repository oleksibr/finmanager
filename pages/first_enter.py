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
        self.add_images_to_layout(left_column, mirrored=False)

        # Права колонка із зображеннями
        right_column = QVBoxLayout()
        self.add_images_to_layout(right_column, mirrored=True)

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
        central_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
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

        # Додати текст і кнопку реєстрації
        label = QLabel("Для початку \nнеобхідно зареєструватися:", self)
        central_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        label.setStyleSheet("""
            QLabel {
                font-size: 30px; 
                font-weight: bold; 
                color: #000000;
                padding: 5px;
                margin-top: 80px;
            }
        """)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        registr_button = QPushButton("Зареєструватися", self)
        registr_button.setStyleSheet(""" 
            QPushButton {
                background-color: #487EF1;
                color: #000000;
                font-size: 24px;
                border-radius: 20px;
                padding: 10px 20px;
                border: 3px solid #000000; 
            }
            QPushButton:hover {
                background-color: #0059b3;
                border: 3px solid #000000;
            }
        """)
        registr_button.setFixedSize(240, 55)
        central_layout.addWidget(registr_button, alignment=Qt.AlignmentFlag.AlignCenter)
        registr_button.clicked.connect(self.handle_registr)

        # Зберегти анімації як атрибути
        self.icon_animation = QPropertyAnimation(self.hand_icon, b"pos")
        self.text_animation = QPropertyAnimation(self.header_label, b"pos")
        self.start_animation()

    def start_animation(self):
        # Анімація для іконки
        self.hand_icon.move(310, 0)
        self.icon_animation.setDuration(2000)
        self.icon_animation.setStartValue(QPoint(310, 0))
        self.icon_animation.setEndValue(QPoint(310, 30))
        self.icon_animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.icon_animation.start()

        # Анімація для тексту
        self.header_label.move(380, 0)
        self.text_animation.setDuration(2000)
        self.text_animation.setStartValue(QPoint(380, 0))
        self.text_animation.setEndValue(QPoint(380, 35))
        self.text_animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.text_animation.start()

    def add_images_to_layout(self, layout, mirrored):
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

    def handle_registr(self):
        from registration import Registration
        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            main_page = Registration()  # Ініціалізуємо сторінку реєстрації
            main_window.setCentralWidget(main_page)  # Замінюємо центральний віджет
            self.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FirstEnter()
    window.showMaximized()
    sys.exit(app.exec())
