from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QComboBox, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QApplication, \
    QMainWindow, QDialog
from PyQt6.QtCore import Qt

from finmanager.models.utils_db import get_list_db
from select_user import SelectUser
from change_existing_db import ChangeDB, load_csv
from delete_existing_db import DeleteDB
from create_new_db import CreateDB
from PyQt6.QtGui import QPixmap, QIcon, QTransform
from Utils import add_images_to_layout
import finmanager.models.utils_db as util
import finmanager.models.models as model
import finmanager.config.config_db as conf




class EntryPage(QWidget):
    def __init__(self):
        super().__init__()

        # Set window background color
        self.setStyleSheet("background-color: #F7F2F2;")

        # Initialize additional windows
        self.create_db_window = None
        self.change_db_window = None
        self.delete_db_window = None

        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.setSpacing(100)

        # Title at the top
        title = QLabel("   ОБЕРІТЬ СИСТЕМУ \nФІНАНСОВИХ ВИТРАТ", self)
        title.setStyleSheet("""
            QLabel {
                font-size: 36px; 
                font-weight: bold; 
                color: #000000;
                padding: 5px, 20px;
                margin-top: 40px;
            }
        """)

        # Left column layout for images
        left_column = QVBoxLayout()
        add_images_to_layout(left_column, mirrored=False)  # Define this method to add images

        # Right column layout for images
        right_column = QVBoxLayout()
        add_images_to_layout(right_column, mirrored=True)  # Define this method to add images

        # Central layout for buttons and database selection
        central_layout = QVBoxLayout()
        central_layout.setSpacing(10)

        # Create the database selection label
        db_label = QLabel("Назва Системи Фінансових Витрат", self)
        db_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        db_label.setStyleSheet("""
            QLabel {
                font-size: 24px; 
                color: #000000; 
                background-color: #E8F0FF;
                border-radius: 20px;
                padding: 10px 20px;
                border: 3px solid #000000;
            }
        """)
        db_label.setFixedSize(450, 60)

        # ComboBox for selecting the database
        self.db_combo = QComboBox(self)
        self.db_combo.addItems(get_list_db())
        conf1 = conf.DatabasesConfig()
        self.db_combo.setCurrentIndex(conf1.get_idx_db_0())
        self.db_combo.setStyleSheet(""" 
            QComboBox {
                background-color: #E8F0FF;
                font-size: 24px;
                padding: 5px 30px 5px 10px;
                color: #000000;
                border: 3px solid #000000;
                border-radius: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #D8EAFC;
                color: #000;
                selection-background-color: #88B9EB;
                selection-color: #D2DDFE;
            }
            QComboBox::drop-down {
                background-color: #B1C3FC;
                border-radius: 15px;
                width: 30px; 
            }
            QComboBox::down-arrow {
                image: url(images/down_arrow.png);
                width: 15px; 
                height: 15px; 
            }
        """)
        self.db_combo.currentIndexChanged.connect(self.handle_db_selection)
        self.db_combo.setFixedSize(450, 60)

        # Add database label and ComboBox to db_layout
        db_layout = QVBoxLayout()
        db_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        db_layout.addWidget(db_label)
        db_layout.addWidget(self.db_combo)

        # Layout for the three buttons
        buttons_layout = QHBoxLayout()


        # Контейнер для кнопок із білим фоном
        buttons_container = QWidget(self)
        buttons_container.setStyleSheet("""
            QWidget {
                background-color: #F7F2F2;
                border: 3px solid #000000;
                border-radius: 20px;
            }
        """)
        buttons_container.setFixedSize(270, 100)  # Розмір контейнера

        # Внутрішній лейаут для кнопок у контейнері
        buttons_inner_layout = QHBoxLayout(buttons_container)
        buttons_inner_layout.setSpacing(15)  # Відстань між кнопками
        buttons_inner_layout.setContentsMargins(10, 10, 10, 10)  # Відступи в контейнері

        # Кнопка для створення нової бази даних
        create_db_btn = QPushButton(buttons_container)
        create_db_btn.setIcon(QIcon("images/addnew.png"))
        create_db_btn.setIconSize(QtCore.QSize(45, 45))
        create_db_btn.setStyleSheet("border: none; background-color: transparent;")
        create_db_btn.clicked.connect(self.open_create_db_window)
        buttons_inner_layout.addWidget(create_db_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка для редагування бази даних
        connect_db_btn = QPushButton(buttons_container)
        connect_db_btn.setIcon(QIcon("images/redact.png"))
        connect_db_btn.setIconSize(QtCore.QSize(45, 45))
        connect_db_btn.setStyleSheet("border: none; background-color: transparent;")
        connect_db_btn.clicked.connect(self.open_change_db_window)
        buttons_inner_layout.addWidget(connect_db_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка для видалення бази даних
        delete_db_btn = QPushButton(buttons_container)
        delete_db_btn.setIcon(QIcon("images/delete.png"))
        delete_db_btn.setIconSize(QtCore.QSize(45, 45))
        delete_db_btn.setStyleSheet("border: none; background-color: transparent;")
        delete_db_btn.clicked.connect(self.open_delete_db_window)
        buttons_inner_layout.addWidget(delete_db_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Додаємо контейнер із кнопками до основного лейаута
        buttons_layout.addWidget(buttons_container, alignment=Qt.AlignmentFlag.AlignCenter)


        # Central layout includes the title, db_layout, buttons, and login button
        central_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        central_layout.addLayout(db_layout)
        central_layout.addLayout(buttons_layout)

        # Login button
        login_button = QPushButton("Увійти", self)
        login_button.setStyleSheet(""" 
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
        login_button.setFixedSize(250, 50)
        central_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        login_button.clicked.connect(self.handle_login)

        # Add left column, central layout, and right column to main layout
        main_layout.addLayout(left_column)
        main_layout.addLayout(central_layout)
        main_layout.addLayout(right_column)

        # Set the main layout for the window
        self.setLayout(main_layout)
    def handle_login(self):
        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            print("Перехід до головного вікна")
            # select_user = SelectUser()  # Створюємо новий віджет
            from main_page import MainPage
            main_page = MainPage()  # Створюємо новий віджет
            # main_window.update_central_widget(select_user)
            # main_window.update_central_widget(main_page)
            main_window.setCentralWidget(main_page)
            self.deleteLater()

    def handle_db_selection(self):
        #selected_db = self.db_combo.itemText(index)
        # selected_db = self.db_combo.setCurrentIndex(index)
        index = self.db_combo.currentIndex()
        conf1 = conf.DatabasesConfig()
        conf1.set_current_db_idx(index)

    def open_create_db_window(self):
        if self.create_db_window is None:
            self.create_db_window = CreateDB()

        # Використовуємо exec() для блокування й отримання результату
        if self.create_db_window.exec() == QDialog.DialogCode.Accepted:
            result = self.create_db_window.result_value
            print(f"Результат: {result}")
            if result == 1:
                list_db = get_list_db()
                self.db_combo.clear()
                self.db_combo.addItems(list_db)
                self.db_combo.setCurrentIndex(len(list_db)-1)
            elif result == 2:
                print("Введення порожнє!")
        else:
            print("Створення бази даних скасовано.")

    def open_change_db_window(self):
        selected_db = self.db_combo.currentText()
        if self.change_db_window is None:
            self.change_db_window = ChangeDB(selected_db)
            self.change_db_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.change_db_window.destroyed.connect(self.clear_change_db_window)
        self.change_db_window.show()

    def open_delete_db_window(self):
        selected_db = self.db_combo.currentText()
        if self.delete_db_window is None:
            self.delete_db_window = DeleteDB(selected_db)
            self.delete_db_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.delete_db_window.destroyed.connect(self.clear_delete_db_window)
        self.delete_db_window.show()

    def clear_create_db_window(self):
        self.create_db_window = None

    def clear_change_db_window(self):
        self.change_db_window = None

    def clear_delete_db_window(self):
        self.delete_db_window = None


if __name__ == '__main__':
    import sys
    import main
    app = QApplication(sys.argv)
    window = main.MainApp()
    sys.exit(app.exec())
