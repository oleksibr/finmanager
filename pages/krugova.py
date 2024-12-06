# from random import random
#
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta
#
# from PyQt6.QtWidgets import QApplication
#
# from finmanager.pages.monthly_widget import PlotGraphDialog
#
#
# def generate_data(start_date, end_date, a, b, c, d, N):
#     start = datetime.strptime(start_date, "%Y-%m-%d")
#     end = datetime.strptime(end_date, "%Y-%m-%d")
#     delta = (end - start).days
#
#     data = []
#     for _ in range(N):
#         random_date = start + timedelta(days=random.randint(0, delta))
#         subconto = random.randint(a, b)
#         summa = random.randint(c, d)
#         data.append([random_date.strftime("%Y-%m-%d"), subconto, summa])
#
#     return data
#
# # Пример данных (или загрузка из файла)
# # data = [
# #     ["2024-01-01", 1, 50],
# #     ["2024-01-01", 2, 30],
# #     ["2024-01-02", 1, 20],
# #     ["2024-01-02", 3, 40],
# #     ["2024-01-03", 2, 70],
# #     ["2024-01-03", 3, 10]
# # ]
# data = generate_data("2024-01-01", "2024-01-30", 1, 3, 10, 100, 10)
# # Создание DataFrame
# df = pd.DataFrame(data, columns=["data", "subconto", "summa"])
#
# # Группируем данные по статьям, суммируя суммы
# grouped = df.groupby("subconto")["summa"].sum().reset_index()
#
# # Подготовка цветовой карты
# subconto_unique = grouped["subconto"].unique()
# colors_map = plt.cm.tab20(np.linspace(0, 1, len(subconto_unique)))
# color_assignment = {subconto: colors_map[i] for i, subconto in enumerate(subconto_unique)}
#
# # Определение цветов для круговой диаграммы
# colors = [color_assignment[subconto] for subconto in grouped["subconto"]]
#
# # Построение круговой диаграммы с числами и процентами
# plt.figure(figsize=(10, 10))
#
# wedges, texts = plt.pie(
#     grouped["summa"],
#     labels=None,  # Убираем стандартные подписи
#     colors=colors,
#     startangle=90,
#     textprops={'fontsize': 10}
# )
#
# # Добавление текста вручную с процентами и числами
# total_sum = grouped["summa"].sum()
# for wedge, row in zip(wedges, grouped.itertuples()):
#     angle = (wedge.theta2 + wedge.theta1) / 2  # Средний угол сектора
#     x = np.cos(np.radians(angle)) * 1.2
#     y = np.sin(np.radians(angle)) * 1.2
#     percent = f"{row.summa / total_sum:.1%}"
#     plt.text(x, y, f"Статья {row.subconto}\n{percent}", ha='center', fontsize=10)
#
# # Настройка графика
# plt.title("Распределение сумм по статьям", fontsize=18)
# plt.tight_layout()
#
# # Сохранение и отображение
# plt.savefig("pie_chart_by_subconto.png", dpi=300)
# plt.show()
#
# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     dialog = PlotGraphDialog()
#     dialog.exec()
