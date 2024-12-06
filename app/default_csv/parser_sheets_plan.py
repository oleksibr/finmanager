from bs4 import BeautifulSoup
import csv
import re

with open("steets_plan.html", "r", encoding="utf-8-sig") as f:  # Додано encoding для обробки UTF-8 файлів
    html_data = f.read()

# Парсинг HTML
soup = BeautifulSoup(html_data, "html.parser")

# Знаходимо всі рядки таблиці
rows = soup.find_all("tr")

# Список для збереження результатів
data = []
kor_sheet = []

# Обробка рядків таблиці
for row in rows[3:]:  # Пропускаємо заголовки
    cells = row.find_all("td")
    if len(cells) < 6:  # Пропускаємо рядки з заголовками класів
        continue

    code_s = cells[0].text.strip()
    назва = cells[1].text.strip()
    субрахунки_html = cells[2].decode_contents().split("<br/>")
    сфера_застосування = cells[5].text.strip()

    data.append(["s", code_s, '', назва, сфера_застосування])
    # Обробляємо субрахунки
    for subaccount_html in субрахунки_html:

        # Використовуємо регулярний вираз для витягнення коду та назви
        match = re.search(r'<strong>(\d+)</strong>\s*(.*)', subaccount_html)
        if match:
            code_ss = match.group(1).strip()
            name = match.group(2).strip()
            data.append(["ss", code_s, code_ss, name, сфера_застосування])
        # subaccount_text = BeautifulSoup(subaccount_html, "html.parser").text.strip()
        # if " " in subaccount_text:
            # номер_субрахунку, назва_субрахунку = subaccount_text.split(" ", 1)
            # data.append([код, назва, номер_субрахунку, назва_субрахунку, сфера_застосування])
        else:
            data.append([code_s.strip(), назва, сфера_застосування])

        [kor_sheet.append([code_s.strip(), sheet_kt.strip()])
         for sheet_kt in cells[3].text.strip().split(",")
         if code_s.strip().isdigit() and sheet_kt.strip().isdigit()]

        [kor_sheet.append([sheet_dt.strip(), code_s.strip()])
         for sheet_dt in cells[3].text.strip().split(",")
         if code_s.strip().isdigit() and sheet_dt.strip().isdigit()]



# Записуємо результат у CSV файл
with open("synthetic_accounts.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=";",  quoting=csv.QUOTE_NONE, escapechar="\\")
    writer.writerow(["type", "s_code", "ss_code", "name", "description"])
    writer.writerows(data)

kor_sheet = list(set(map(tuple, kor_sheet)))
kor_sheet = [list(item) for item in kor_sheet]
with open("kor_sheets_table.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=";", quoting=csv.QUOTE_NONE, escapechar="\\")
    writer.writerow(["sheet_dt", "sheet_kt"])
    writer.writerows(kor_sheet)

print("CSV файл створено: synthetic_accounts.csv")
