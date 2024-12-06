import csv
import os
from datetime import datetime, timedelta
from random import random

import numpy as np
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QHBoxLayout, QLineEdit, QSpacerItem,
                             QSizePolicy, QStackedWidget, QListWidget, QMainWindow, QComboBox, QDialog, QFileDialog,
                             QMessageBox, QInputDialog, QTableWidget, QTableWidgetItem, QGraphicsView, QGraphicsScene,
                             QGraphicsRectItem, QDateEdit, QHeaderView)
from PyQt6.QtCore import Qt, QSize, QUrl, QDate
from PyQt6.QtGui import QIcon, QColor, QDesktopServices, QPixmap
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.uic.Compiler.qtproxies import QtWidgets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas

from finmanager.pages.change_existing_db import load_csv
from user_window import UserWindow
from PyQt6 import QtCore
import finmanager.models.utils_db as util
import finmanager.models.models as model
import finmanager.config.config_db as conf
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime





class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""\
            QPushButton {
                background-color: #B1C3FC;
                color: #000000;
                font-size: 18px;
                border-radius: 20px;
                padding: 10px 20px;
                border: 3px solid #000000;
            }
            QPushButton:hover {
                background-color: #406CF6;
                border: 3px solid #FFFFFF;
            }
        """)
        self.setFixedSize(200, 50)

class CustomComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(""" 
                                QComboBox {
                                    background-color: #E8F0FF;
                                    font-size: 14px;
                                    padding: 5px 15px 5px 10px;
                                    color: #000000;
                                    border-radius: 5px;
                                }
                                QComboBox QAbstractItemView {
                                    background-color: #D8EAFC;
                                    color: #000;
                                    selection-background-color: #88B9EB;
                                    selection-color: #D2DDFE;
                                }
                                QComboBox::drop-down {
                                    background-color: #B1C3FC;
                                    border-radius: 5px;
                                    width: 20px; 
                                }
                                QComboBox::down-arrow {
                                    image: url(images/down_arrow.png);
                                    width: 14px; 
                                    height: 14px; 
                                }
                            """)
        self.setFixedSize(110, 30)

class DocumentViewWindow(QDialog):
    def __init__(self, document_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(document_name)
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        label = QLabel(f"Document: {document_name}")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        # Dropdown (ComboBox) inside the document view window
        dropdown = CustomComboBox()
        dropdown.addItems(["Option 1", "Option 2", "Option 3"])  # Example items
        layout.addWidget(dropdown)

        self.setLayout(layout)


class WindowWhenClickedEdit(QDialog):
    def __init__(self, parent=None, id_doc=None, name_list_type_doc=None):
        super().__init__(parent)
        self.setWindowTitle("Редагування")
        self.setFixedSize(1100, 700)
        self.setStyleSheet("background-color: #F7F2F2")

        # Таблиця
        self.table = QTableWidget(1, 9, self)
        self.table.hideColumn(8)
        spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)


        self.table.setHorizontalHeaderLabels([
            "Номер", "Тип операції", "Субконта", "Кількість", "Ціна", "Сума", "Валюта", "Коментар", "operation_id"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setFixedHeight(450)
        self.table.setFixedWidth(800)
        self.table.setStyleSheet("""
                    QTableWidget {
                        background-color: #E8F0FF;
                        color: #000000;
                        gridline-color: #D3D3D3;
                        font-size: 14px;
                        border: 1px solid #000000;
                    }
                    QHeaderView::section {
                        background-color: #4682B4;
                        color: white;
                        font-weight: bold;
                        border: 1px solid #000000; 
                    }
                     QTableWidget::item {
                        border: 1px solid #000000;  
                    }
                """)

        combo_box = QComboBox()
        combo_box.addItems(["Продаж", "Закупівля", "Обмін", "Інше"])  # Приклад варіантів
        self.table.setCellWidget(0, 1, combo_box)


class WindowWhenClickedDelete(QDialog):
    def __init__(self, parent=None, id_doc=None, name_list_type_doc=None):
        super().__init__(parent)
        self.setWindowTitle("Видалення")
        self.setFixedSize(1200, 400)
        self.setStyleSheet("background-color: #F7F2F2;")

        # Таблиця
        self.table = QTableWidget(1, 9, self)
        self.table.hideColumn(8)
        spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.table.setHorizontalHeaderLabels([
            "Номер", "Тип операції", "Субконта", "Кількість", "Ціна", "Сума", "Валюта", "Коментар", "operation_id"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setFixedHeight(150)
        self.table.setFixedWidth(1200)
        self.table.setStyleSheet("""
                            QTableWidget {
                                background-color: #E8F0FF;
                                color: #000000;
                                gridline-color: #D3D3D3;
                                font-size: 14px;
                                border: 1px solid #000000;
                            }
                            QHeaderView::section {
                                background-color: #4682B4;
                                color: white;
                                font-weight: bold;
                                border: 1px solid #000000; 
                            }
                             QTableWidget::item {
                                border: 1px solid #000000;  
                            }
                        """)
        combo_box = QComboBox()
        combo_box.addItems(["Продаж", "Закупівля", "Обмін", "Інше"])  # Приклад варіантів
        self.table.setCellWidget(0, 1, combo_box)


class DocumentCreationWindow(QDialog):
    def __init__(self, parent=None, id_doc=None, name_list_type_doc=None):
        super().__init__(parent)
        self.setWindowTitle("Створити документ")
        # self.showMaximized()
        self.setFixedSize(1000, 700)

        self.id_doc, self.name_list_type_doc = util.get_document_types()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)

        # Центральний макет
        central_layout = QVBoxLayout()

        # Поле ID (приховане поле)
        # self.id_label = QLabel("ID:", self)
        # self.id_label.setStyleSheet("font-size: 18px;color: #000000;")
        # central_layout.addWidget(self.id_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Календар
        self.date_input = QDateEdit(self)
        self.date_input.setDisplayFormat('yyyy-MM-dd')  # Формат дати
        self.date_input.setDate(QDate.currentDate())  # Поточна дата як дефолт
        self.date_input.setStyleSheet("""
                   QDateEdit {
                       font-size: 18px;
                       padding: 5px;
                       background-color: #E8F0FF;
                       border: 2px solid #000000;
                       color: #000000;
                   }
               """)
        self.date_input.setFixedSize(160, 40)
        self.date_input.setCalendarPopup(True)
        self.date_input.setContentsMargins(70, 0, 10, 0)

        # Отримуємо календарний віджет і застосовуємо стилі
        calendar = self.date_input.calendarWidget()
        if calendar:
            calendar.setStyleSheet("""
                    QCalendarWidget QWidget{
                        background-color: #487EF1;
                        color: black;

                        }

                    QCalendarWidget QToolButton{
                        background-color:#487EF1;
                        color: black;
                        icon-size: 20px;
                        }

                    QCalendarWidget QMenu{
                        background-color:#487EF1;
                        color: black;

                        }

                    QCalendarWidget QAbstractItemView:enabled{
                        background-color: #487EF1;
                        color: black;
                        }

                    QCalendarWidget QAbstractItemView:disabled{
                        background-color: #487EF1;
                        color: white;
                        }

                    QCalendarWidget QMenu{
                            background-color: #487EF1;
                        }

                    QCalendarWidget QSpinBox{
                            background-color: black;
                        }
                   """)
        else:
            print("Не вдалося знайти календар!")

        central_layout.addWidget(self.date_input, alignment=Qt.AlignmentFlag.AlignRight)

        # Комбо-бокс для типу документу
        self.label1 = QLabel("Документ:", self)
        self.label1.setFixedSize(90, 40)
        self.label1.setStyleSheet("font-size: 18px; color: #000000")
        central_layout.addWidget(self.label1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.type_combo = QComboBox(self)
        self.type_combo.addItems(self.name_list_type_doc)
        self.type_combo.setStyleSheet("""
                            QComboBox {
                                background-color: #E8F0FF;
                                font-size: 18px;
                                padding: 5px 20px 5px 10px;
                                color: #000000;
                                border: 2px solid #000000;
                            }
                            QComboBox QAbstractItemView {
                                background-color: #D8EAFC;
                                color: #000;
                                selection-background-color: #88B9EB;
                                selection-color: #D2DDFE;
                            }
                        """)
        self.type_combo.setFixedSize(240, 40)
        central_layout.addWidget(self.type_combo, alignment=Qt.AlignmentFlag.AlignLeft)

        self.summ_label = QLabel("Сума загалом: 12345", self)
        self.summ_label.setStyleSheet("font-size: 18px;color: #000000;")
        self.summ_label.setFixedSize(180, 40)
        self.summ_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Поле для коментаря
        self.comm_input = QLineEdit(self)
        self.comm_input.setPlaceholderText("Введіть коментар")
        self.comm_input.setStyleSheet("""
            font-size: 18px;
            padding: 5px;
            background-color: #FFFFFF;
            border: 2px solid #000000;
            border-radius: 15px;
            color: #000000;
        """)
        self.comm_input.setFixedSize(560, 40)
        self.comm_input.setContentsMargins(11, 0, 0, 0)
        central_layout.addWidget(self.comm_input, alignment=Qt.AlignmentFlag.AlignRight)

        # Поле для QR-коду
        self.inc_qr_code = QLineEdit(self)
        self.inc_qr_code.setPlaceholderText("QRcode")
        self.inc_qr_code.setStyleSheet("""
                    font-size: 18px;
                    padding: 5px;
                    background-color: #FFFFFF;
                    border: 2px solid #000000;
                    border-radius: 15px;
                    color: #000000;
                """)
        self.inc_qr_code.setFixedSize(140, 40)
        self.inc_qr_code.setContentsMargins(10, 0, -7, 0)
        central_layout.addWidget(self.inc_qr_code, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка завантажити QR код
        self.inc_qr_butt = QPushButton("Загрузити", self)
        self.inc_qr_butt.setStyleSheet("""
                    QPushButton {
                        background-color: #487EF1;
                        color: #000000;
                        font-size: 14px;
                        border-radius: 15px;
                        padding: 10px 10px;
                        border: 2px solid #000000;
                    }
                    QPushButton:hover {
                        background-color: #406CF6;
                        border: 2px solid #FFFFFF;
                    }
                """)
        self.inc_qr_butt.setFixedSize(100, 40)
        self.inc_qr_butt.setContentsMargins(0, 0, 70, 0)
        central_layout.addWidget(self.inc_qr_butt, alignment=Qt.AlignmentFlag.AlignLeft)

        row1_layout = QHBoxLayout()
        row1_layout.addWidget(self.date_input)
        row1_layout.addWidget(self.label1)
        row1_layout.addWidget(self.type_combo)
        row1_layout.addWidget(self.summ_label)

        # Вторая строка Layout
        row2_layout = QHBoxLayout()

        row2_layout.addWidget(self.comm_input)
        row2_layout.addWidget(self.inc_qr_code)
        row2_layout.addWidget(self.inc_qr_butt)
        # main_layout.addLayout(row3_layout)

        # Таблиця
        self.table = QTableWidget(1, 11, self)
        self.table.hideColumn(10)

        self.table.setHorizontalHeaderLabels([
            "Номер", "Тип операції", "Субконта", "Кількість", "Ціна", "Сума", "Валюта", "Коментар", "Редагування",
            "Видалення", "operation_id"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setFixedHeight(300)
        self.table.setStyleSheet("""
                    QTableWidget {
                        background-color: #E8F0FF;
                        color: #000000;
                        gridline-color: #D3D3D3;
                        font-size: 14px;
                        border: 1px solid #000000;
                    }
                    QHeaderView::section {
                        background-color: #487EF1;
                        color: white;
                        font-weight: bold;
                        border: 1px solid #000000; 
                    }
                     QTableWidget::item {
                        border: 1px solid #000000;  
                    }
                """)
        edit_button = QPushButton("Редагувати", self)
        edit_button.setStyleSheet(
            "padding: 5px; font-size: 14px;color:#000000; border-color: #000000; border: 1px solid;")
        delete_button = QPushButton("Видалити", self)
        delete_button.setStyleSheet(
            "padding: 5px; font-size: 14px;color:#000000; border-color: #000000; border: 1px solid;")

        self.table.setCellWidget(0, 8, edit_button)
        self.table.setCellWidget(0, 9, delete_button)

        self.table.setItem(0, 0, QTableWidgetItem("tjkht"))
        # ddd = QPushButton("ffffff", self)
        # self.table.setItem(0,1, QTableWidget(ddd))
        # Створення кнопки
        ddd = QPushButton("ffffff", self)
        self.table.setCellWidget(0, 1, ddd)

        # central_layout.addWidget(self.table)

        # Створюємо кнопку "плюс"
        image_button = QPushButton(self)
        pixmap = QPixmap("images/plus.png")
        image_button.setIcon(QIcon(pixmap))
        image_button.setStyleSheet("border: none;")
        image_button.setFixedSize(20, 20)
        image_button.clicked.connect(self.add_operation_row)

        # Кнопки збереження та скасування
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        cancel_button = QPushButton("Скасувати", self)
        cancel_button.setStyleSheet("""
                    QPushButton {
                        background-color: #487EF1;
                        color: #000000;
                        font-size: 14px;
                        border-radius: 15px;
                        padding: 10px 10px;
                        border: 2px solid #000000;
                    }
                    QPushButton:hover {
                        background-color: #406CF6;
                        border: 2px solid #FFFFFF;
                    }
                """)
        cancel_button.clicked.connect(self.cancel_doc_creat)
        cancel_button.setFixedSize(160, 40)

        create_as_button = QPushButton("Зберегти чернетку", self)
        create_as_button.setStyleSheet("""
                            QPushButton {
                                background-color: #487EF1;
                                color: #000000;
                                font-size: 14px;
                                border-radius: 15px;
                                padding: 10px 10px;
                                border: 2px solid #000000;
                            }
                            QPushButton:hover {
                                background-color: #406CF6;
                                border: 2px solid #FFFFFF;
                            }
                        """)
        create_as_button.clicked.connect(self.save_as_doc_creat)
        create_as_button.setFixedSize(160, 40)

        create_button = QPushButton("Зберегти", self)
        create_button.setStyleSheet("""
            QPushButton {
                background-color: #487EF1;
                color: #000000;
                font-size: 14px;
                border-radius: 15px;
                padding: 10px 10px;
                border: 2px solid #000000;
            }
            QPushButton:hover {
                background-color: #406CF6;
                border: 2px solid #FFFFFF;
            }
        """)
        create_button.clicked.connect(self.save_doc_creat)
        create_button.setFixedSize(160, 40)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(create_button)
        button_layout.addWidget(create_as_button)

        # Добавляем строки в основной Layout
        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)
        main_layout.addWidget(self.table)
        # Додаємо макет кнопки одразу після таблиці
        main_layout.addWidget(image_button, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def add_operation_row(self):
        # self.table.insertRow(0)
        # self.table.setItem(2, 2, "test")
        row_count = self.table.rowCount() + 1
        self.table.setRowCount(row_count)
        self.update()

    def clicked_table(self, row, col):
        if col == 8:
            self.add_operation_row()
            print(self.table.rowCount())
            self.table.setItem(row, 10, QTableWidgetItem("row"))
        elif col == 9:
            print(self.table.item(row, 10).text())
            pass

    def save_doc(self):
        pass

    def cancel_doc(self):
        pass
    def open_edit_window(self):
        if not self.edit_window:  # Перевіряємо, чи вікно вже не відкрите
            self.edit_window = WindowWhenClickedEdit(self)
        self.edit_window.show()

    def open_delete_window(self):
        if not self.delete_window:  # Перевіряємо, чи вікно вже не відкрите
            self.delete_window = WindowWhenClickedDelete(self)
        self.delete_window.show()
    def cancel_doc_creat(self):
        pass

    def save_as_doc_creat(self):
        pass

    def save_doc_creat(self):
        pass


class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Головна сторінка")
        self.setStyleSheet("background-color: #F7F2F2;")

        self.selected_button = None

        # Основний вертикальний лейаут
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Створення хедера
        header = QFrame()
        header.setStyleSheet("background-color: #75A1FF;")
        header.setFixedHeight(55)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 10, 0)

        hand_icon = QLabel(header)
        hand_icon.setPixmap(QIcon("images/financial.png").pixmap(30, 30))
        header_layout.addWidget(hand_icon, alignment=Qt.AlignmentFlag.AlignLeft)

        header_label = QLabel("Financial cost\nmanagement system", header)
        header_layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignRight)
        header_label.setStyleSheet("font-size: 14px; color: #000000; font-weight: bold;")
        header_layout.addWidget(header_label)

        header_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        search_box = QLineEdit(header)
        search_box.setPlaceholderText("Search...")
        search_box.setFixedHeight(30)
        search_box.setFixedWidth(400)
        search_box.setStyleSheet("""
            background-color: #D5DDF7;
            color: #000000;
            border: 2px solid #000000;
            border-radius: 15px;
            padding: 5px 10px;
            font-size: 14px;
        """)

        header_layout.addWidget(search_box, alignment=Qt.AlignmentFlag.AlignCenter)

        header_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        # name = util.create_user()
        #
        # user_name_label = QLabel(f"Логін користувача: {name}", header)
        #
        # user_name_label.setStyleSheet("font-size: 14px; color: #000000; font-weight: bold;")
        # header_layout.addWidget(user_name_label, alignment=Qt.AlignmentFlag.AlignRight)

        user_button = QPushButton(header)
        user_button.setIcon(QIcon("images/user.png"))
        user_button.setIconSize(QtCore.QSize(30, 30))
        user_button.setStyleSheet("border: none; background-color: transparent;")
        user_button.clicked.connect(self.open_user_window)  # Прив'язуємо функцію відкриття UserWindow
        header_layout.addWidget(user_button, alignment=Qt.AlignmentFlag.AlignRight)


        settings_icon = QPushButton(header)
        settings_icon.setIcon(QIcon("images/settings_icon.png"))
        settings_icon.setIconSize(QtCore.QSize(30, 30))
        settings_icon.setStyleSheet("border: none; background-color: transparent;")
        settings_icon.clicked.connect(self.go_to_entry_page)
        header_layout.addWidget(settings_icon, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(header)

        # Бокова панель з кнопками
        side_panel = QFrame()
        side_panel.setStyleSheet("background-color: #d3e1fa;")
        side_panel_layout = QVBoxLayout(side_panel)
        side_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.documents_button = CustomButton("Документи", self)
        self.documents_button.clicked.connect(self.show_documents_widget)
        side_panel_layout.addWidget(self.documents_button)

        self.operations_button = CustomButton("Операції", self)
        self.operations_button.clicked.connect(self.show_operations_widget)
        side_panel_layout.addWidget(self.operations_button)

        self.reports_button = CustomButton("Звіти", self)
        self.reports_button.clicked.connect(self.show_reports_widget)
        side_panel_layout.addWidget(self.reports_button)

        self.monthly_expenses_button = CustomButton("Витрати за місяць", self)
        self.monthly_expenses_button.clicked.connect(self.show_monthly_expenses_widget)
        side_panel_layout.addWidget(self.monthly_expenses_button)

        self.expense_accounts_button = CustomButton("План рахунків", self)
        self.expense_accounts_button.clicked.connect(self.show_expense_accounts_widget)
        side_panel_layout.addWidget(self.expense_accounts_button)

        # self.magazines_button = CustomButton("Журнали", self)
        # self.magazines_button.clicked.connect(self.show_magazines_widget)
        # side_panel_layout.addWidget(self.magazines_button)

        # Стек для відображення різного функціоналу
        self.stacked_widget = QStackedWidget()

        self.operations_widget = self.create_operations_widget()
        self.reports_widget = self.create_reports_widget()
        self.monthly_expenses_widget = self.create_monthly_expenses_widget()
        self.expense_accounts_widget = self.create_expense_accounts_widget()
        self.documents_widget = self.create_documents_widget()
        self.magazines_widget = self.create_magazines_widget()

        empty_widget = QWidget()  # Можна додати відповідний віджет чи макет
        self.stacked_widget.addWidget(empty_widget)

        # Додаємо віджети в стек
        self.stacked_widget.addWidget(self.operations_widget)
        self.stacked_widget.addWidget(self.reports_widget)
        self.stacked_widget.addWidget(self.monthly_expenses_widget)
        self.stacked_widget.addWidget(self.expense_accounts_widget)
        self.stacked_widget.addWidget(self.documents_widget)
        self.stacked_widget.addWidget(self.magazines_widget)

        # Центральний контентний блок
        content_area = QFrame()
        content_area.setStyleSheet("background-color: #FFFFFF;")
        content_area_layout = QVBoxLayout(content_area)
        content_area_layout.addWidget(self.stacked_widget)

        # Горизонтальний лейаут для бокової панелі та центрального контенту
        central_layout = QHBoxLayout()
        central_layout.addWidget(side_panel)
        central_layout.addWidget(content_area)
        central_layout.setStretch(1, 1)

        main_layout.addLayout(central_layout)

        footer = QFrame()
        footer.setStyleSheet("background-color: #B5BDD9;")
        footer.setFixedHeight(40)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(10, 0, 10, 0)

        footer_label = QLabel("Кошти на рахунку: ", footer)
        footer_label.setStyleSheet("font-size: 16px; color: #000000;")
        footer_layout.addWidget(footer_label)

        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def select_button(self, button):
        if self.selected_button:
            self.selected_button.setStyleSheet("""\
                        QPushButton {
                            background-color: #B1C3FC;
                            color: #000000;
                            font-size: 18px;
                            border-radius: 20px;
                            padding: 10px 20px;
                            border: 3px solid #000000;
                        }
                        QPushButton:hover {
                            background-color: #406CF6;
                        }
                    """)
        button.setStyleSheet("""\
                    QPushButton {
                        background-color: #406CF6;
                        color: #FFFFFF;
                        font-size: 18px;
                        border-radius: 20px;
                        padding: 10px 20px;
                        border: 3px solid #000000;
                    }
                    QPushButton:hover {
                        background-color: #B1C3FC;
                        color: #000000;
                    }
                """)
        self.selected_button = button

    def show_documents_widget(self):
        self.stacked_widget.setCurrentWidget(self.documents_widget)
        self.select_button(self.documents_button)

    def show_operations_widget(self):
        self.stacked_widget.setCurrentWidget(self.operations_widget)
        self.select_button(self.operations_button)

    def show_reports_widget(self):
        self.stacked_widget.setCurrentWidget(self.reports_widget)
        self.select_button(self.reports_button)

        #ddd = util.list_parent(model.Account, 2)
        #print(ddd)

    def show_monthly_expenses_widget(self):
        self.stacked_widget.setCurrentWidget(self.monthly_expenses_widget)
        self.select_button(self.monthly_expenses_button)

    def show_expense_accounts_widget(self):
        self.stacked_widget.setCurrentWidget(self.expense_accounts_widget)
        self.select_button(self.expense_accounts_button)

    # def show_magazines_widget(self):
    #     self.stacked_widget.setCurrentWidget(self.magazines_widget)
    #     self.select_button(self.magazines_button)

    def open_document(self, item):
        document_name = item.text()
        self.document_view_window = DocumentViewWindow(document_name, self)
        self.document_view_window.show()

    def open_document_creation_window(self):
        self.document_creation_window = DocumentCreationWindow(self)
        self.document_creation_window.show()

    def add_document_to_list(self, document_name):
        self.document_list.addItem(document_name)

    def ddd(self):
        pass

    def create_documents_widget(self):
        """"
        Class Document:
            id; - добавить как невидимое поле
            number; user_number; - сделать через дефис
            date; edited_date; - обрати останню
            summ_dt; summ_kt; - поставить знак +-
            type_id; - получить как текст
            comment_id; - получить текст коментария
            status; - получить нейм как текст(проведен/непроведен/черновик)

            creator_id;
            editor_id;
            lock;
            income_qr_code;
        """
        widget = QWidget()
        main_layout = QHBoxLayout()  # Головний лейаут для віджета

        # Створення вертикального лейаута для таблиці та її напису
        table_layout = QVBoxLayout()

        label_layout = QHBoxLayout()

        # Додавання іконки над написом "Документи"
        info_button = QPushButton()
        info_button.setIcon(QIcon("images/i.png"))  # Замініть на шлях до вашої іконки
        info_button.setIconSize(QSize(20, 20))
        info_button.setStyleSheet("border: none;")  # Забираємо рамку у кнопки
        info_button.setCursor(Qt.CursorShape.PointingHandCursor)
        info_button.clicked.connect(self.show_documents_info)

        # Лейбл для таблиці
        self.label2 = QLabel("Документи:", self)
        self.label2.setStyleSheet("font-size: 26px; color: #000000; margin-bottom: 1px;")  # Додано верхній відступ
        label_layout.addWidget(self.label2, alignment=Qt.AlignmentFlag.AlignRight)
        label_layout.addWidget(info_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Додаємо горизонтальний лейаут з іконкою та написом до вертикального
        table_layout.addLayout(label_layout)

        self.table_widget = QTableWidget(10, 8, self)
        self.table_widget.cellDoubleClicked.connect(self.open_document_by_click)
        self.table_widget.setHorizontalHeaderLabels([
            "Номер", "Дата", "Дебіт", "Кредит", "Сума", "Статус", "Тип документу",
             "Коментар"
        ])

        self.table_widget.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #E8F0FF;
                font-size: 14px;
                font-weight: bold;
                color: #000000;
                padding: 5px;
                border-radius: 15px;
                border: 2px solid #000000;
            }
        """)

        # Приховуємо вертикальні заголовки
        self.table_widget.verticalHeader().setVisible(False)

        # Стиль для таблиці (округлення кутів)
        self.table_widget.setStyleSheet("""
            QTableWidget {
                font-size: 16px;
                color: #000000;
                background-color: #FFFFFF;
                border: 3px solid #000000;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        self.table_widget.setFixedSize(980, 550)

        # Задання висоти рядків і ширини колонок
        row_height = 40  # Висота рядка
        column_width = 120  # Ширина колонки

        for row in range(self.table_widget.rowCount()):
            self.table_widget.setRowHeight(row, row_height)  # Встановлюємо висоту кожного рядка

        for column in range(self.table_widget.columnCount()):
            self.table_widget.setColumnWidth(column, column_width)  # Встановлюємо ширину кожної колонки


        # Додавання прикладових даних та комбобоксів
        for row in range(self.table_widget.rowCount()):
            self.table_widget.setItem(row, 0, QTableWidgetItem(f"Документ {row + 1}"))
            current_date = datetime.now().strftime("%Y-%m-%d")

            self.table_widget.setItem(row, 1, QTableWidgetItem(current_date))

            self.table_widget.cellClicked.connect(self.cell_was_clicked)



            self.db_combo = CustomComboBox()
            self.db_combo.addItems(util.list_parent(model.Account, 1))
            conf1 = conf.DatabasesConfig()
            self.db_combo.setCurrentIndex(conf1.get_idx_db_0())

            # Підключаємо сигнал зміни вибору
            self.db_combo.currentIndexChanged.connect(lambda index, r=row: self.ddd(r, index))

            # Додаємо QComboBox у таблицю
            self.table_widget.setCellWidget(row, 2, self.db_combo)

            self.db_combo1 = CustomComboBox()
            self.db_combo1.addItems(util.list_parent(model.Account, 1))
            conf1 = conf.DatabasesConfig()
            self.db_combo1.setCurrentIndex(conf1.get_idx_db_0())

            # Підключаємо сигнал зміни вибору
            self.db_combo1.currentIndexChanged.connect(lambda index, r=row: self.ddd(r, index))

            # Додаємо QComboBox у таблицю
            self.table_widget.setCellWidget(row, 3, self.db_combo1)
        table_layout.addWidget(self.table_widget)  # Додаємо таблицю під напис


        # Лейаут для кнопок
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        button_width = 180
        button_layout.setContentsMargins(0, 60, 0, 0)
        create_button = self.create_custom_button("Створити", button_width)
        add_button = self.create_custom_button("Редагувати", button_width)
        delete_button = self.create_custom_button("Видалити", button_width)
        rename_button = self.create_custom_button("Перейменувати", button_width)

        create_button.clicked.connect(self.open_document_creation_window)
        add_button.clicked.connect(self.add_document)
        delete_button.clicked.connect(self.delete_document)
        rename_button.clicked.connect(self.rename_document)

        button_layout.addWidget(create_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(rename_button)

        # Додаємо лейаут для таблиці та кнопок до головного лейаута
        main_layout.addLayout(table_layout)  # Додаємо таблицю з написом до головного лейаута
        main_layout.addLayout(button_layout)  # Додаємо кнопки праворуч

        widget.setLayout(main_layout)
        return widget

    def cell_was_clicked(self, row, column):
        print("Row %d and Column %d was clicked" % (row, column))


    def open_document_by_click(self, row, column):
        """Обробка кліку по комірці таблиці."""
        # Перевіряємо, чи клікнули на колонку з назвами (колонка 0)
        if column == 0:  # Індекс колонки з назвами документів
            document_name = self.table_widget.item(row, column).text()  # Отримуємо назву документа
            document_path = f"documents/{document_name}.pdf"  # Формуємо шлях до документа

            # Відкриваємо документ, якщо файл існує
            if os.path.exists(document_path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(document_path))
            else:
                QMessageBox.warning(self, "Помилка", f"Документ '{document_name}' не знайдено.")

    def create_combo_box(self):
        combo_box = QComboBox(self)
        combo_box.addItems(["1", "2", "3"])  # Додаємо елементи 1, 2, 3
        combo_box.setStyleSheet("""
            QComboBox {
                background-color: #F1F1F1;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                color: #000000;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #CCCCCC;
                selection-background-color: #A1C3FF;
                selection-color: #000000;
            }
        """)
        return combo_box

    def create_operations_widget(self):
        widget = QWidget()
        layout = QHBoxLayout()

        # Лейбл для розділу
        label = QLabel("Операції", self)
        label_layout = QHBoxLayout()
        label_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #000000; font-size: 26px; margin-bottom: 20px;")  # Додано нижній відступ
        layout.addWidget(label)

        # Створення кнопок
        button_width = 180
        create_button = self.create_custom_button("Створити", button_width)
        add_button = self.create_custom_button("Додати", button_width)
        delete_button = self.create_custom_button("Видалити", button_width)
        rename_button = self.create_custom_button("Перейменувати", button_width)

        # Підключення кнопок до функцій

        # Додавання кнопок до лейауту
        layout.addWidget(create_button)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)
        layout.addWidget(rename_button)

        # Налаштовуємо віджет
        widget.setLayout(layout)
        return widget

    def create_reports_widget(self):
        widget = QWidget()
        main_layout = QHBoxLayout()  # Головний лейаут для віджета

        # Створення вертикального лейаута для таблиці та її напису
        table_layout = QVBoxLayout()

        # Лейбл для таблиці
        label = QLabel("Звіти:", self)
        label.setStyleSheet("font-size: 26px; color: #000000; margin-bottom: 1px;")  # Додано верхній відступ
        table_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)  # Центрування напису

        # Створення таблиці
        self.table_widget = QTableWidget(10, 4, self)
        self.table_widget.setHorizontalHeaderLabels([
            "Назва", "Дата",
            "Статус", "Коментар"
        ])


        self.table_widget.horizontalHeader().setStyleSheet("""
                    QHeaderView::section {
                        background-color: #E8F0FF;
                        font-size: 14px;
                        font-weight: bold;
                        color: #000000;
                        padding: 5px;
                        border-radius: 15px;
                        border: 2px solid #000000;
                    }
                """)

        # Приховуємо вертикальні заголовки
        self.table_widget.verticalHeader().setVisible(False)

        # Стиль для таблиці (округлення кутів)
        self.table_widget.setStyleSheet("""
                    QTableWidget {
                        font-size: 16px;
                        color: #000000;
                        background-color: #FFFFFF;
                        border: 3px solid #000000;
                    }
                    QTableWidget::item {
                        padding: 5px;
                    }
                """)
        self.table_widget.setFixedSize(500, 300)

        # Задання висоти рядків і ширини колонок
        row_height = 40  # Висота рядка
        column_width = 120  # Ширина колонки

        for row in range(self.table_widget.rowCount()):
            self.table_widget.setRowHeight(row, row_height)  # Встановлюємо висоту кожного рядка

        for column in range(self.table_widget.columnCount()):
            self.table_widget.setColumnWidth(column, column_width)  # Встановлюємо ширину кожної колонки

        # Додавання прикладових даних
        for row in range(self.table_widget.rowCount()):
            self.table_widget.setItem(row, 0, QTableWidgetItem(f"Звіт {row + 1}"))
            self.table_widget.setItem(row, 1, QTableWidgetItem("2024-11-25"))

        table_layout.addWidget(self.table_widget)  # Додаємо таблицю під напис

        # Лейаут для кнопок
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        button_width = 180
        button_layout.setContentsMargins(0, 60, 0, 0)
        create_button1 = self.create_custom_button("Створити", button_width)
        add_button1 = self.create_custom_button("Додати", button_width)
        delete_button1 = self.create_custom_button("Видалити", button_width)
        rename_button1 = self.create_custom_button("Перейменувати", button_width)

        button_layout.addWidget(create_button1)
        button_layout.addWidget(add_button1)
        button_layout.addWidget(delete_button1)
        button_layout.addWidget(rename_button1)

        # Додаємо лейаут для таблиці та кнопок до головного лейаута
        main_layout.addLayout(table_layout)  # Додаємо таблицю з написом до головного лейаута
        # main_layout.addLayout(button_layout)  # Додаємо кнопки праворуч

        widget.setLayout(main_layout)
        return widget


    def create_monthly_expenses_widget(self):
        """Метод для створення віджета з графіком витрат за місяць."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Лейбл для опису
        label = QLabel("Витрати за місяць:")
        label.setStyleSheet("font-size: 26px; color: #000000; margin-bottom: 1px;")  # Додано верхній відступ
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)  # Центруван

        # Створення графічного виду для графіка
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene)
        view.setFixedSize(1000, 600)

        # Дані для графіка
        categories = ["Оренда житла", "Харчування", "Транспорт", "Комун. послуги", "Здоров'я", "Розваги",
                      "Інші витрати"]
        expenses = [120, 450, 300, 150, 200, 100, 50]
        max_expense = max(expenses)
        width = 80  # Ширина стовпця
        spacing = 100  # Відстань між стовпцями

        for i, expense in enumerate(expenses):
            height = (expense / max_expense) * 400  # Масштабування висоти
            x_pos = i * spacing

            # Створення стовпця
            color = self.get_column_color(expense, max_expense)
            rect = QGraphicsRectItem(x_pos, 500 - height, width, height)
            rect.setBrush(color)
            scene.addItem(rect)

            # Додавання підпису категорії
            text_item = scene.addText(categories[i])
            text_item.setPos(x_pos, 510)
            text_item.setDefaultTextColor(QColor(0, 0, 0))

        layout.addWidget(view)
        return widget

        # button_layout = QHBoxLayout()
    #
    #
    #     graph_button = QPushButton("Графік")
    #     pie_chart_button = QPushButton("Кругова діаграма")
    #     pie_chart_button.setStyleSheet("""\
    #                 QPushButton {
    #                     background-color: #B1C3FC;
    #                     color: #000000;
    #                     font-size: 18px;
    #                     border-radius: 20px;
    #                     padding: 10px 20px;
    #                     border: 3px solid #000000;
    #                 }
    #                 QPushButton:hover {
    #                     background-color: #406CF6;
    #                     border: 3px solid #FFFFFF;
    #                 }
    #             """)
    #     graph_button.setStyleSheet("""\
    #                 QPushButton {
    #                     background-color: #B1C3FC;
    #                     color: #000000;
    #                     font-size: 18px;
    #                     border-radius: 20px;
    #                     padding: 10px 20px;
    #                     border: 3px solid #000000;
    #                 }
    #                 QPushButton:hover {
    #                     background-color: #406CF6;
    #                     border: 3px solid #FFFFFF;
    #                 }
    #             """)
    #
    #     graph_button.setFixedSize(200, 50)
    #     pie_chart_button.setFixedSize(200, 50)
    #
    #     button_layout.addWidget(graph_button)
    #     button_layout.addWidget(pie_chart_button)
    #     layout.addWidget(graph_button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    #     layout.addWidget(pie_chart_button, alignment=Qt.AlignmentFlag.AlignRight| Qt.AlignmentFlag.AlignTop)
    #
    #     layout.addLayout(button_layout)
    #
    #     return widget





    def get_column_color(self, expense, max_expense):
        """Градієнт синього: менші витрати — світліший колір, більші — темніший."""
        intensity = 1 - (expense / max_expense)  # Зворотна інтенсивність (чим менше витрати, тим більше інтенсивність)
        color_value = int(255 * intensity)  # Світліший синій для менших витрат
        return QColor(0, 0, color_value)  # Використовуємо лише синій канал

    def clear_content_area(self):
        """Очищає область контенту перед відображенням нового віджета."""
        while self.content_area.count():
            child = self.content_area.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # id;
    # parent_id;
    # number;
    # name;
    # description;
    # type_id;
    # status_id;
    # lock_id;
    # subcounto_id;
    # edited_date;
    # history_list_id
    def create_expense_accounts_widget(self):
        # Створюємо основний віджет і компоновку
        widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel("План рахунків:")
        label.setStyleSheet("font-size: 26px; color: #000000; margin-bottom: 1px;")  # Додано верхній відступ
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)  # Центрування

        # Створюємо таблицю
        table = QTableWidget(1, 7)
        table.setHorizontalHeaderLabels([
            "ID", "Рахунок", "Субрахунок", "Субконта", "Статус", "Опис", "Тип операції"
        ])

        table.setFixedSize(950, 500)
        table.setColumnWidth(0, 120)  # ID
        table.setColumnWidth(1, 120)  # Рахунок
        table.setColumnWidth(2, 120)  # Субрахунок
        table.setColumnWidth(3, 120)  # Субконта
        table.setColumnWidth(4, 120)  # Статус
        table.setColumnWidth(5, 120)  # Опис
        table.setColumnWidth(6, 120)  # Тип операції
        layout.addWidget(table, alignment=Qt.AlignmentFlag.AlignCenter)

        # Додаємо стилі заголовків
        table.horizontalHeader().setStyleSheet("""
                                    QHeaderView::section {
                                        background-color: #E8F0FF;
                                        font-size: 14px;
                                        font-weight: bold;
                                        color: #000000;
                                        padding: 5px;
                                        border-radius: 15px;
                                        border: 2px solid #000000;
                                    }
                                """)

        # Приховуємо вертикальні заголовки
        table.verticalHeader().setVisible(False)

        # Стиль для таблиці (округлення кутів)
        table.setStyleSheet("""
                                    QTableWidget {
                                        font-size: 16px;
                                        color: #000000;
                                        background-color: #FFFFFF;
                                        border: 3px solid #000000;
                                    }
                                    QTableWidget::item {
                                        padding: 5px;
                                    }
                                """)
        table.setFixedSize(950, 400)


        data = util.get_list_accouts()
        for i, row in enumerate(data):
            table.addItem(0, 0, )
        table.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                table.setItem(row_index, column_index, QTableWidgetItem(cell_data))

        # Додаємо таблицю в макет
        layout.addWidget(table)

        widget.setLayout(layout)

        return widget

    def create_magazines_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Це сторінка для журналів.")
        label.setStyleSheet("color: #000000; font-size: 26px")
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def create_custom_button(self, text, width):
        button = CustomButton(text, self)
        button.setFixedWidth(width)
        return button

    def open_user_window(self):
        self.user_window = UserWindow()
        self.user_window.show()

    def go_to_entry_page(self):
        from entry_page import EntryPage
        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            entry_page = EntryPage()
            main_window.setCentralWidget(entry_page)
            self.deleteLater()


    def add_document(self):
        """Відкрити вікно вибору файлу і додати документ до списку."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Оберіть документ",
            "",
            "Документи (*.docx *.pdf *.txt *.xlsx);;Усі файли (*)"
        )

        if file_path:  # Якщо файл обрано
            file_name = file_path.split("/")[-1]  # Отримати лише ім'я файлу
            self.document_list.addItem(file_name)  # Додати файл до списку

            # Інформаційне повідомлення
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Файл додано")
            msg_box.setText(f"Документ '{file_name}' успішно додано.")
            msg_box.setStyleSheet("""
                QMessageBox {
                    font-size: 14px;
                }
                QMessageBox QLabel {
                    color: #000000;
                }
                QMessageBox QPushButton {
                    background-color: #406CF6;
                        color: #FFFFFF;
                        font-size: 14px;
                        border-radius: 10px;
                        padding: 5px 10px;
                        border: 2px solid #000000;
                }
                QMessageBox QPushButton:hover {
                    background-color: #D0D0D0;
                }
            """)
            msg_box.exec()
        else:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Додавання скасовано")
            msg_box.setText("Ви не обрали жодного документа.")
            msg_box.setStyleSheet("""
                QMessageBox {
                    font-size: 14px;
                }
                QMessageBox QLabel {
                    color: #000000;
                }
                QMessageBox QPushButton {
                    background-color: #406CF6;
                        color: #FFFFFF;
                        font-size: 14px;
                        border-radius: 10px;
                        padding: 5px 10px;
                        border: 2px solid #000000;
                }
                QMessageBox QPushButton:hover {
                    background-color: #D0D0D0;
                }
            """)
            msg_box.exec()

    def delete_document(self):
        """Видалити вибраний документ зі списку."""
        selected_item = self.document_list.currentItem()

        # Створюємо один об'єкт QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox {
                color: #000000;  # Чорний текст
                font-size: 16px;
                border: 2px solid #A1A1A1;
                border-radius: 10px;
                padding: 20px;
            }
            QPushButton {
                background-color: #406CF6;  # Синя кнопка
                color: #FFFFFF;
                font-size: 14px;
                border-radius: 10px;
                padding: 5px 10px;
                border: 2px solid #000000;
            }
            QPushButton:hover {
                background-color: #D0D0D0;  # При наведенні світлішає
            }
        """)

        if selected_item:
            # Створення питання для підтвердження видалення
            reply = msg_box.question(
                self,
                "Підтвердження видалення",
                f"Ви дійсно хочете видалити документ '{selected_item.text()}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                row = self.document_list.row(selected_item)
                self.document_list.takeItem(row)

                # Повідомлення про успішне видалення
                msg_box.information(self, "Документ видалено", f"Документ '{selected_item.text()}' успішно видалено.")
            elif reply == QMessageBox.StandardButton.No:
                # Повідомлення про скасування видалення
                msg_box.information(self, "Видалення скасовано", "Видалення документа скасовано.")
        else:
            # Якщо документ не вибрано, відобразити попередження
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Помилка")
            msg_box.setText("Будь ласка, виберіть документ для видалення.")
            msg_box.setStyleSheet("""
                QMessageBox {
                    font-size: 14px;
                }
                QMessageBox QLabel {
                    color: #000000;
                }
                QMessageBox QPushButton {
                    background-color: #406CF6;
                    color: #FFFFFF;
                    font-size: 14px;
                    border-radius: 10px;
                    padding: 5px 10px;
                    border: 2px solid #000000;
                }
                QMessageBox QPushButton:hover {
                    background-color: #D0D0D0;
                }
            """)
            msg_box.exec()  # Запускаємо виконання модального вікна

    def show_documents_info(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Інформація про документи")
        msg_box.setText(
            "<span style='color: black;'>"
            "Документи – це файли, що містять важливі дані, такі як назва, сума, статус тощо."
            "</span>"
        )

        # Додаємо стиль для кнопок
        msg_box.setStyleSheet("""
            QMessageBox {
                font-size: 14px;
                color: black;
            }
            QPushButton {
                background-color: #E8F0FF;
                font-size: 14px;
                font-weight: bold;
                color: #000000;
                padding: 4px;
                border-radius: 10px;
                border: 2px solid #000000;
            }
            QPushButton:hover {
                background-color: #D0E0FF;
            }
            QPushButton:pressed {
                background-color: #B0C8FF;
            }
        """)

        msg_box.exec()

    def rename_document(self):
        """Перейменувати вибраний документ."""
        selected_item = self.document_list.currentItem()

        if selected_item:
            new_name, ok = QInputDialog.getText(
                self,
                "Перейменувати документ",
                "Введіть нову назву документа:",
                text=selected_item.text()
            )

            QInputDialog.setStyleSheet(self, """
                QInputDialog {
                    background-color: #F5F5F5;
                    color: #000000;
                    font-size: 16px;
                    border: 2px solid #A1A1A1;
                    border-radius: 10px;
                    padding: 20px;
                }
                QLineEdit {
                    font-size: 14px;
                    background-color: #FFFFFF;
                    color: #000000;
                }
                QInputDialog QPushButton {
                    background-color: #406CF6;
                        color: #FFFFFF;
                        font-size: 14px;
                        border-radius: 10px;
                        padding: 5px 10px;
                        border: 2px solid #000000;
                }
                QInputDialog QPushButton:hover {
                    background-color: #D0D0D0;
                }
            """)

            if ok and new_name:
                selected_item.setText(new_name)

                QMessageBox.information(self, "Документ перейменовано", f"Документ успішно перейменовано на '{new_name}'.")
            elif not new_name:
                QMessageBox.warning(self, "Помилка", "Ви не ввели нову назву документа.")
        else:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Помилка")
            msg_box.setText("Будь ласка, виберіть документ для перейменування.")
            msg_box.setStyleSheet("""
                               QMessageBox {
                                   font-size: 14px;
                               }
                               QMessageBox QLabel {
                                   color: #000000;
                               }
                               QMessageBox QPushButton {
                                   background-color: #406CF6;
                                       color: #FFFFFF;
                                       font-size: 14px;
                                       border-radius: 10px;
                                       padding: 5px 10px;
                                       border: 2px solid #000000;
                               }
                               QMessageBox QPushButton:hover {
                                   background-color: #D0D0D0;
                               }
                           """)
            msg_box.exec()


class MyTable(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table_widget = QtWidgets.QTableWidget()

        self.setCentralWidget(self.table_widget)

        # Устанавливаем количество строк и столбцов в таблице
        self.table_widget.setRowCount(5)
        self.table_widget.setColumnCount(3)

        # Создаем цикл для добавления чекбоксов в каждую ячейку таблицы
        for row in range(self.table_widget.rowCount()):
            for column in range(self.table_widget.columnCount()):
                checkbox_item = QtWidgets.QTableWidgetItem(str(row))
                if column == 2:
                    checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    checkbox_item.setCheckState(Qt.CheckState.Unchecked)
                    checkbox_item.setText('')
                self.table_widget.setItem(row, column, checkbox_item)

    def eventFilter(self, source, event):
        print(event)
if __name__ == '__main__':
    import sys
    import main
    app = QApplication(sys.argv)
    window = main.MainApp()
    sys.exit(app.exec())