import csv
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QDialog
from PyQt6.QtCore import Qt
import os


import csv

def load_csv(file_csv):
    data = []
    with open(file_csv, mode="r", newline="", encoding="utf-8") as ps:
        reader = csv.reader(ps, delimiter=';')
        next(reader)
        for row in reader:
            data.append(row)

    return [name[1] for name in data]


class ChangeDB(QDialog):
    def __init__(self, selected_db=""):
        super().__init__()
        self.setWindowTitle("Зміна системи")
        self.setFixedSize(600, 300)
        self.setStyleSheet("background-color: #F7F2F2;")

        # Основний вертикальний лейаут
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(5)  # Загальний простір між елементами, зменшений

        # Підпис і назва обраної БД
        selected_db_label = QLabel("Обрана система фінансових витрат:", self)
        selected_db_label.setStyleSheet("font-size: 20px; color: #000000; font-weight: bold;")
        main_layout.addSpacing(20)
        main_layout.addWidget(selected_db_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.selected_db_display = QLabel(selected_db, self)
        self.selected_db_display.setStyleSheet("""
            QLabel {
                font-size: 16px; 
                color: #000000; 
                background-color: #FFFFFF; 
                padding: 5px 10px;
                border-radius: 20px;
                border: 2px solid #000000;    
            }
        """)
        self.selected_db_display.setFixedSize(300, 40)
        main_layout.addWidget(self.selected_db_display, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(10)  # Зменшений проміжок між назвою БД та наступним елементом

        # Текстовий надпис для введення нової назви
        label = QLabel("Введіть нову назву системи:", self)
        label.setStyleSheet("font-size: 20px; color: #000000; font-weight: bold;")
        main_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Поле вводу для нової назви з меншим відступом до надпису
        self.db_name_input = QLineEdit(self)
        self.db_name_input.setPlaceholderText("Нова назва системи")
        self.db_name_input.setFixedSize(300, 40)
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
        main_layout.addWidget(self.db_name_input, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(60)  # Додаємо трохи простору перед кнопками

        # Горизонтальний лейаут для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)  # Простір між кнопками
        # Кнопка для скасування
        cancel_button = QPushButton("Відміна", self)
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
        cancel_button.setFixedSize(170, 50)
        cancel_button.clicked.connect(self.close)  # Закриває поточне вікно
        buttons_layout.addWidget(cancel_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Кнопка для зміни назви
        changedb_button = QPushButton("Змінити назву", self)
        changedb_button.setStyleSheet(""" 
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
        changedb_button.setFixedSize(170, 50)
        buttons_layout.addWidget(changedb_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Додаємо лейаут кнопок до основного лейауту
        main_layout.addLayout(buttons_layout)

        # Встановлюємо основний лейаут для віджету
        self.setLayout(main_layout)

# Запуск додатку
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChangeDB("test")
    window.show()
    sys.exit(app.exec())
