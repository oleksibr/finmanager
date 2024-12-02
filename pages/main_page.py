import os

import numpy as np
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QHBoxLayout, QLineEdit, QSpacerItem,
                             QSizePolicy, QStackedWidget, QListWidget, QMainWindow, QComboBox, QDialog, QFileDialog,
                             QMessageBox, QInputDialog, QTableWidget, QTableWidgetItem, QGraphicsView, QGraphicsScene,
                             QGraphicsRectItem)
from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtGui import QIcon, QColor, QDesktopServices
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
                                    font-size: 16px;
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


class DocumentCreationWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Створити документ")
        self.setFixedSize(300, 230)

        layout = QVBoxLayout()

        # Input for document name
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Введіть назву")
        self.name_input.setStyleSheet("""
            font-size: 16px;
            padding: 5px;
            background-color: #FFFFFF;
            border: 2px solid #d3d3d3;
            border-radius: 10px;
            color: #000000;
        """)
        self.name_input.setFixedSize(250, 40)
        layout.addWidget(self.name_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.label1 = QLabel("Оберіть тип документу:", self)
        self.label1.setStyleSheet("font-size: 16px; font-weight: bold; color: #000000")
        layout.addWidget(self.label1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.type_combo = QComboBox(self)
        path_csv = "/pages/csv/default_doc_types.csv"
        self.type_combo.addItems(load_csv(path_csv))
        self.type_combo.setStyleSheet(""" 
                    QComboBox {
                        background-color: #E8F0FF;
                        font-size: 16px;
                        padding: 5px 20px 5px 10px;
                        color: #000000;
                        border: 2px solid #000000;
                        border-radius: 10px;
                    }
                    QComboBox QAbstractItemView {
                        background-color: #D8EAFC;
                        color: #000;
                        selection-background-color: #88B9EB;
                        selection-color: #D2DDFE;
                    }
                    QComboBox::drop-down {
                        background-color: #B1C3FC;
                        border-radius: 10px;
                        width: 30px; 
                    }
                    QComboBox::down-arrow {
                        image: url(images/down_arrow.png);
                        width: 15px; 
                        height: 15px; 
                    }
                """)
        self.type_combo.setFixedSize(250, 40)
        layout.addWidget(self.type_combo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create button
        create_button = QPushButton("Створити", self)
        create_button.clicked.connect(self.create_document)
        create_button.setStyleSheet(""" 
            QPushButton {
                background-color: #B1C3FC;
                color: #000000;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px 10px;
                border: 2px solid #000000;
            }
            QPushButton:hover {
                background-color: #406CF6;
                border: 2px solid #FFFFFF;
            }
        """)
        create_button.setFixedSize(160, 40)
        layout.addWidget(create_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def create_document(self):
        document_name = self.name_input.text()
        if document_name:
            # Signal to create the document in the main window
            self.parent().add_document_to_list(document_name)
            self.close()



class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Головна сторінка")
        self.setStyleSheet("background-color: #F7F2F2;")
        self.showMaximized()

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

        user_name_label = QLabel("{login}", header)
        user_name_label.setStyleSheet("font-size: 14px; color: #000000; font-weight: bold;")
        header_layout.addWidget(user_name_label, alignment=Qt.AlignmentFlag.AlignRight)

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

        self.expense_accounts_button = CustomButton("Рахунки витрат", self)
        self.expense_accounts_button.clicked.connect(self.show_expense_accounts_widget)
        side_panel_layout.addWidget(self.expense_accounts_button)

        self.magazines_button = CustomButton("Журнали", self)
        self.magazines_button.clicked.connect(self.show_magazines_widget)
        side_panel_layout.addWidget(self.magazines_button)

        # Стек для відображення різного функціоналу
        self.stacked_widget = QStackedWidget()

        self.operations_widget = self.create_operations_widget()
        self.reports_widget = self.create_reports_widget()
        self.monthly_expenses_widget = self.create_monthly_expenses_widget()
        self.expense_accounts_widget = self.create_expense_accounts_widget()
        self.documents_widget = self.create_documents_widget()
        self.magazines_widget = self.create_magazines_widget()

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

        footer_label = QLabel("Кошти на рахунку: {money_on_acc}", footer)
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

        # Методи для відображення відповідних віджетів

    def show_documents_widget(self):
        self.stacked_widget.setCurrentWidget(self.documents_widget)
        self.select_button(self.documents_button)

    def show_operations_widget(self):
        self.stacked_widget.setCurrentWidget(self.operations_widget)
        self.select_button(self.operations_button)

    def show_reports_widget(self):
        pass

        #ddd = util.list_parent(model.Account, 2)
        #print(ddd)

    def show_monthly_expenses_widget(self):
        self.stacked_widget.setCurrentWidget(self.monthly_expenses_widget)
        self.select_button(self.monthly_expenses_button)

    def show_expense_accounts_widget(self):
        self.stacked_widget.setCurrentWidget(self.expense_accounts_widget)
        self.select_button(self.expense_accounts_button)

    def show_magazines_widget(self):
        self.stacked_widget.setCurrentWidget(self.magazines_widget)
        self.select_button(self.magazines_button)

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

        self.table_widget = QTableWidget(16, 8, self)
        self.table_widget.cellDoubleClicked.connect(self.open_document_by_click)
        self.table_widget.setHorizontalHeaderLabels([
            "Номер", "Назва", "Дебіт", "Кредит", "Дата", "Сума",
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
        self.table_widget.setFixedSize(980, 600)

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
            self.table_widget.setItem(row, 5, QTableWidgetItem("2024-11-25"))

            self.db_combo = CustomComboBox()
            self.db_combo.addItems(util.list_parent(model.Account, 2))
            conf1 = conf.DatabasesConfig()
            self.db_combo.setCurrentIndex(conf1.get_idx_db_0())

            # Підключаємо сигнал зміни вибору
            self.db_combo.currentIndexChanged.connect(lambda index, r=row: self.ddd(r, index))

            # Додаємо QComboBox у таблицю
            self.table_widget.setCellWidget(row, 2, self.db_combo)

            self.db_combo1 = CustomComboBox()
            self.db_combo1.addItems(util.list_parent(model.Account, 2))
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
        table_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)  # Центрування напису

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
                align: center;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        self.table_widget.setFixedSize(980, 600)

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
        main_layout.addLayout(button_layout)  # Додаємо кнопки праворуч

        widget.setLayout(main_layout)
        return widget

    # def create_monthly_expenses_widget(self):
    #     widget = QWidget()
    #
    #     return widget

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

    def create_expense_accounts_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Це сторінка для рахунків витрат.")
        label.setStyleSheet("color: #000000; font-size: 26px")
        layout.addWidget(label)
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
