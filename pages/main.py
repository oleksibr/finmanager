import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from select_user import SelectUser

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #F2F2F2;
            }
        """)

        # Головний віджет для MainWindow
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Менеджер компоновки для центрального віджета
        self.layout = QVBoxLayout(self.central_widget)

        # Створюємо SelectUser і додаємо його до компоновки
        self.select_user = SelectUser()
        self.layout.addWidget(self.select_user)

        # Налаштування головного вікна
        self.setWindowTitle("Financial cost management system")
        self.showMaximized()


    def update_central_widget(self, widget):
        """Метод для оновлення центрального віджета."""
        self.layout.removeWidget(self.central_widget)
        self.central_widget.deleteLater()  # Видалення старого віджета
        self.central_widget = widget
        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec())

