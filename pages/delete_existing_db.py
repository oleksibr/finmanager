import os

from PyQt6.QtWidgets import QDialog, QMessageBox, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
import finmanager.models.utils_db as util

class DeleteDB(QDialog):
    def __init__(self, selected_db=""):
        super().__init__()

        self.selected_db = selected_db
        self.setWindowTitle("Видалення системи")
        self.setStyleSheet("background-color: #F7F2F2;")
        self.setFixedSize(600, 300)

        # Основний лейаут
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Лейбл з повідомленням
        message_label = QLabel(
            f"Ви справді хочете видалити \n систему фінансових витрат: '{self.selected_db}'?", self
        )
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet("font-size: 20px; color: #000000; padding: 20px; font-weight: bold;")
        layout.addWidget(message_label)

        # Горизонтальний макет для кнопок
        button_layout = QHBoxLayout()

        # Кнопка підтвердження
        delete_button = QPushButton("Видалити", self)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #FFB6C1;
                color: #000000;
                font-size: 18px;
                border-radius: 20px;
                padding: 10px 20px;
                border: 3px solid #000000;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF0000;
                border: 3px solid #FFFFFF;
            }
        """)
        delete_button.setFixedSize(150, 50)
        delete_button.clicked.connect(self.confirm_delete)
        button_layout.addWidget(delete_button)

        # Кнопка скасування
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
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def confirm_delete(self):
       pass
