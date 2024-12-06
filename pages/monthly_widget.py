from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

# Генерація даних
def generate_data(start_date, end_date, a, b, c, d, N):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = (end - start).days

    data = []
    for _ in range(N):
        random_date = start + timedelta(days=random.randint(0, delta))
        subconto = random.randint(a, b)
        summa = random.randint(c, d)
        data.append([random_date.strftime("%Y-%m-%d"), subconto, summa])

    return data

class PlotGraphDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графік витрат")
        self.setGeometry(100, 100, 800, 600)

        # Макет і компоненти
        layout = QVBoxLayout(self)

        # Полотно для графіка
        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)

        # Кнопка для побудови графіка
        self.button = QPushButton("Побудувати графік")
        layout.addWidget(self.button)

        # Підключення кнопки до функції
        self.button.clicked.connect(self.plot_graph)

    def plot_graph(self):
        """Функція для побудови графіка."""
        # Генерація даних
        data = generate_data('2024-01-01', '2024-01-10', 1, 3, 10, 100, 10)
        df = pd.DataFrame(data, columns=["data", "subconto", "summa"])
        result = df.groupby(["data", "subconto"], as_index=False).sum()
        sorted_days = sorted(result["data"].unique())
        result["data_idx"] = result["data"].apply(lambda x: sorted_days.index(x) + 1)

        subconto_unique = result["subconto"].unique()
        colors_map = plt.cm.tab20(np.linspace(0, 1, len(subconto_unique)))
        color_assignment = {subconto: colors_map[i] for i, subconto in enumerate(subconto_unique)}

        # Побудова графіка
        ax = self.canvas.figure.subplots()
        ax.clear()

        for day, group in result.groupby("data_idx"):
            x_position = day
            cumulative_bottom = 0
            for _, row in group.iterrows():
                subconto = row["subconto"]
                value = row["summa"]
                color = color_assignment[subconto]
                ax.bar(x_position, value, bottom=cumulative_bottom, color=color, width=0.6, alpha=0.7)
                ax.text(x_position, cumulative_bottom + value / 2, str(subconto), ha='center', va='center',
                        fontsize=8)
                cumulative_bottom += value
            ax.text(x_position, cumulative_bottom + 5, str(cumulative_bottom), ha='center', va='bottom',
                    fontsize=10, fontweight='bold')

        ax.set_xlabel('Дні місяця', fontsize=12)
        ax.set_ylabel('Сума витрат', fontsize=12)
        day_labels = [datetime.strptime(day, "%Y-%m-%d").day for day in sorted_days]
        ax.set_xticks(range(1, len(sorted_days) + 1))
        ax.set_xticklabels(day_labels, rotation=0, fontsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.6)

        legend_labels = [f"Стаття {subconto}" for subconto in subconto_unique]
        ax.legend(
            handles=[plt.Rectangle((0, 0), 1, 1, color=color_assignment[subconto]) for subconto in subconto_unique],
            labels=legend_labels, loc='upper left', bbox_to_anchor=(1, 1))

        self.canvas.figure.tight_layout()
        self.canvas.draw()

# Запуск програми
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = PlotGraphDialog()
    dialog.exec()
