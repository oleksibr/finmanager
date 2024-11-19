from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout


def replace_page(stack, old, new):
    stack.removeWidget(old)
    new.show()
    stack.addWidget(new)

    stack.setCurrentWidget(new)

    old.hide()

def add_images_to_layout(layout, mirrored):
    layout.setSpacing(0)  # Налаштування відстані між елементами
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
            48, 48,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))

        # Контейнер для вирівнювання
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(10, 0, 10, 0)  # Налаштування відступів
        container_layout.setSpacing(0)

        if i % 3 == 0:  # Вирівнювання ліворуч з меншим відступом
            container_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignLeft)
        elif i % 3 == 1:  # Вирівнювання праворуч з більшим відступом
            container_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignRight)
        else:
            container_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Додавання контейнера до основного лейауту
        layout.addWidget(container)
