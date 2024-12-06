import os
import json
import csv
from datetime import datetime

from sqlalchemy import func, text, inspect
from sqlalchemy.exc import IntegrityError
# from models.models import Level, Account, AccountType, AssociatedAccount, Base
from sqlalchemy.orm import declarative_base
import finmanager.config.config_db as conf_db
import finmanager.models.models as model
from finmanager.models.evgeniy_utils_part1 import create_user, get_user_by_id, get_all_users, delete_user, get_accounts_by_parent_id, get_document_types, create_empty_document, get_document_status, set_document_status
# from evgeniy_utils_part1 import *

# dd = get_user_by_id(1)
# print(dd.name)

# root_dt_values = model.AssociatedAccount.find_all_record_kt(session, 30)
# root_kt_values = model.AssociatedAccount.find_all_record_dt(session, 30)
#UI
def list_parent(in_model, id):
    """
    list_parent(model.Account, 10)
    :param in_model:
    :param id:
    :return:
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()
    descendants = session.query(
            in_model
        ).filter(
            in_model.parent_id == id
        ).all()
    session.close()
    list = [name.name for name in descendants]
    print(list)
    return list


def get_id_by_name(session, model, name):
    """id запису по збігу поля name."""
    record = session.query(model.id).filter(model.name == name).first()
    return record[0] if record else None


def get_sheet_id_by_number(session, model, sheet_number):
    """id запису по збігу поля name."""
    record = session.query(model.id).filter(model.number == sheet_number).first()
    return record[0] if record else None


def generate_next_number(session, model):
    max_number = session.query(func.max(model.number)).scalar() or 0
    return max_number + 1


def get_dict_classes_models():
    table_classes_name = {
        "AccountBalance": model.AccountBalance,
        "AccountType": model.AccountType,
        "Account": model.Account,
        "AssociatedAccount": model.AssociatedAccount,
        "Comment": model.Comment,
        "Currency": model.Currency,
        "DocumentType": model.DocumentType,
        "Document": model.Document,
        "HistoryAccount": model.HistoryAccount,
        "AccessLevel": model.AccessLevel,
        "Operation": model.Operation,
        "QrCode": model.QrCode,
        "ScTransactionType": model.ScTransactionType,
        "ScTransaction": model.ScTransaction,
        "Status": model.Status,
        "SubcountoBalance":model.SubcountoBalance,
        "SubcountoType":model.SubcountoType,
        "Subcounto":model.Subcounto,
        "TransactionType": model.TransactionType,
        "Transaction": model.Transaction,
        "Unit": model.Unit,
        "User": model.User
    }
    return table_classes_name


#GUI
def get_list_db():
    """
    load "list_db":  from config.json

    :return ({dict},{dict}, ... {dict})

    [{"name": "name_db_0", "path": "path_db_0" },
    {"name": "name_db_1", "path1": "path_db_1" },
    ... ,
    {..., ...}]
    """
    config = conf_db.DatabasesConfig()
    return [val["db_name"] for val in config.get_list_db()]


def check_file_name_match(file_name, folder_path):

    new_name_db_base = os.path.splitext(file_name)[0]

    for filename in os.listdir(folder_path):
        file_base = os.path.splitext(filename)[0]

        if file_base.lower() == new_name_db_base.lower():
            return True
    return False


def get_data_from_csv(file_csv):
    data = []
    with open(file_csv, mode="r", newline="", encoding="utf-8-sig") as ps:
        reader = csv.DictReader(ps, delimiter=';')

        # Очищаємо ключі (імена стовпців) від BOM-символів
        fieldnames = [field.lstrip('\ufeff') for field in reader.fieldnames]

        for row in reader:
            row = {fieldnames[i]: value for i, value in enumerate(row.values())}

            if 'date' in row:
                if not row['date']:
                    row['date'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                row['date'] = datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%S')

            if 'edited_date' in row:
                if not row['edited_date']:
                    row['edited_date'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                row['edited_date'] = datetime.strptime(row['edited_date'], '%Y-%m-%dT%H:%M:%S')

            data.append(row)
    return data


#Ui
def create_default_db(new_name_db=None):
    config = conf_db.DatabasesConfig()
    dir_db = config.work_dir

    if new_name_db and check_file_name_match(new_name_db, dir_db):
        return 1
    elif new_name_db == None:
        i = ''
        good_name = False
        while good_name == False:
            for item in config.get_list_db():
                good_name = True
                name = os.path.splitext(item['db_name'])[0]
                if f"default_db{i}" == name:
                    good_name = False
                    i = 1 if i == '' else i
                    i += 1
                    break
        new_name_db = "default_db.db" if i == 0 else f"default_db{i}.db"

    # dir_csv = config.get_csv_dir()
    # if os.path.isdir(dir_csv)==None:
    #     print (f"dir csv: {dir_csv} - not found")

    default_csv_list = [
        "..\\default_csv\\AccessLevel.csv",
        "..\\default_csv\\AccountBalance.csv",
        "..\\default_csv\\AccountType.csv",
        "..\\default_csv\\Account.csv",
        "..\\default_csv\\AssociatedAccount.csv",
        "..\\default_csv\\Comment.csv",
        "..\\default_csv\\Currency.csv",
        "..\\default_csv\\DocumentType.csv",
        "..\\default_csv\\Document.csv",
        "..\\default_csv\\HistoryAccount.csv",
        "..\\default_csv\\Operation.csv",
        "..\\default_csv\\QrCode.csv",
        "..\\default_csv\\ScTransactionType.csv",
        "..\\default_csv\\ScTransaction.csv",
        "..\\default_csv\\Status.csv",
        "..\\default_csv\\SubcountoBalance.csv",
        "..\\default_csv\\Subcounto.csv",
        "..\\default_csv\\SubcountoType.csv",
        "..\\default_csv\\TransactionType.csv",
        "..\\default_csv\\Transaction.csv",
        "..\\default_csv\\User.csv",
        "..\\default_csv\\Unit.csv"
    ]

    print(f"new_name_db:{new_name_db}")
    print(f"config.get_cur_db_name(): {config.get_cur_db_name()}")
    print(f"config.db_path: {config.get_path_db()}")
    # print(f"config.db_name {config.name_db}")
    print(f"config.idx_db_0: {config.current_db_idx}")


    tabele_class = get_dict_classes_models()
    engine = config.create_new_db(new_name_db)

    for file_csv in default_csv_list:
        class_name = os.path.splitext(os.path.basename(file_csv))[0]
        cur_class = tabele_class[class_name]

        data = get_data_from_csv(file_csv)
        try:
            config = conf_db.DatabasesConfig()
            session = config.create_session()

            for row in data:
                add(session, cur_class, **row)

            session.commit()  # ФіКС зміни в базі даних

        except Exception as e:
            if session:
                session.rollback()  # У разі помилки відкатуємо зміни
            print(f"Помилка: {e}")
        finally:
            if session:
                session.close()
    return


def delete_all_row_reset_id(model_table):

    config = conf_db.DatabasesConfig()
    session = config.create_session()

    session.execute(text(f"DELETE FROM {model_table}"))
    session.commit()
    session.close()

    # # Скидання автоінкременту для SQLite
    # session = config.create_session()
    # session.execute(text(f"DELETE FROM sqlite_sequence WHERE name='{model_table}'"))
    # session.commit()
    # session.close()


def add(session, model_class, **kwargs):
    """
    Універсальна функція для додавання нового рядка до будь-якої моделі.
    Підтримує моделі з кастомними методами save() або validate().
    :param session: SQLAlchemy session
    :param model_class: Клас моделі (наприклад, Account)
    :param kwargs: Аргументи для створення нового об'єкта
    :return: Доданий об'єкт
    """

    if 'session' in model_class.__init__.__code__.co_varnames:
        new_instance = model_class(session=session, **kwargs)
    else:
        new_instance = model_class(**kwargs)

    try:
        if hasattr(new_instance, "unique_name"):
            new_instance.unique_name(kwargs)


        if hasattr(new_instance, "validdate"):
            new_instance.validate(kwargs, session=session)


        else:
            # Стандартне збереження
            session.add(new_instance)
            # session.commit()

        print(f"Added {model_class.__name__}: {kwargs}")
        return new_instance
    except Exception as e:
        session.rollback()
        raise ValueError(f"Error adding {model_class.__name__}: {e}")


# UI
def add_data_from_single_csv(full_path_file_csv):
    """
    add_data_from_single_csv("..\\default_csv\\AssociatedAccount.csv")
    :param full_path_file_csv:
    :return:
    """
    if not full_path_file_csv:
        return 1

    class_name = os.path.splitext(os.path.basename(full_path_file_csv))[0]
    data = []
    with open(full_path_file_csv, mode="r", newline="", encoding="utf-8-sig") as ps:
        reader = csv.DictReader(ps, delimiter=';')

        # Очищаємо ключі (імена стовпців) від BOM-символів
        fieldnames = [field.lstrip('\ufeff') for field in reader.fieldnames]

        for row in reader:
            row = {fieldnames[i]: value for i, value in enumerate(row.values())}

            if 'date' in row:
                if not row['date']:
                    row['date'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                row['date'] = datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%S')

            if 'edited_date' in row:
                if not row['edited_date']:
                    row['edited_date'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                row['edited_date'] = datetime.strptime(row['edited_date'], '%Y-%m-%dT%H:%M:%S')

            data.append(row)

    tabele_class = get_dict_classes_models()
    cur_class = tabele_class[class_name]

    try:
        config = conf_db.DatabasesConfig()
        session = config.create_session()

        for row in data:
            add(session, cur_class, **row)

        session.commit()  # Підтверджуємо зміни в базі даних
    except Exception as e:
        if session:
            session.rollback()  # У разі помилки відкатуємо зміни
        print(f"Помилка: {e}")
    finally:
        if session:
            session.close()
    return


#TODO
def edite_access_level(new_name=None, new_level=None, id = None, user = None):
    """
        Оновлює рівень доступу в базі даних.

        :param new_name: Нове ім'я рівня доступу (необов'язковий)
            яущо передати new_name = '' - ім'я видалить.
        :param new_level: Новий рівень доступу (необов'язковий).
        :param id: ID рівня доступу (необов'язковий).
        :param user: Ім'я рівня доступу для пошуку (необов'язковий).
        :return: None
        """
    if not (new_name or new_level):
        return

    config = conf_db.DatabasesConfig()
    session = config.create_session()
    if id:
        level = session.query(model.AccessLevel).filter_by(id=id).first()
        if level:
            level.edit_level(session, access_level=new_level, name=new_name)
    elif user:
        level = session.query(model.AccessLevel).filter_by(name='user').first()
        if level:
            level.edit_level(session, access_level=new_level, name=new_name)

    return

    # @staticmethod
    # def delete_level(level_id, session):
    #     """
    #     Видаляє рівень доступу за ID.
    #     """
    #     try:
    #         level = session.query(AccessLevel).filter_by(id=level_id).first()
    #         if not level:
    #             raise ValueError(f"No AccessLevel found with id={level_id}.")
    #
    #         session.delete(level)
    #         session.commit()
    #         print(f"AccessLevel with id={level_id} deleted successfully.")
    #     except Exception as e:
    #         session.rollback()
    #         raise ValueError(f"Error deleting AccessLevel: {e}")


# create_default_db("test")
# create_default_db()

# delete_all_row_reset_id("AssociatedAccount")
# add_data_from_single_csv("..\default_csv\AssociatedAccount.csv")

# edite_access_level("admin","r","admin")

# config = conf_db.DatabasesConfig()
# session = config.create_session()
# session.query(model.Account).filter(model.Account.id != None).delete()
# session.commit()
# session.close()

# config = conf_db.DatabasesConfig()
# session = config.create_session()
# doc = session.get(model.Document, 1)
# name = doc.get_doc_name(session)
# print(name)

#Отримати поля таблиці
# config = conf_db.DatabasesConfig()
# session = config.get_db_engine()
# with session.connect() as connection:
#     result = connection.execute(text("PRAGMA table_info(docums);"))
#     result2 = connection.execute(text("PRAGMA table_info(statuses);"))
#     for row in result2:
#         print(row)
#     for row in result:
#         print(row)


# date_str = '2024-11-29 02:30:47.499445'
# converted_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
# print(converted_date)  # 2024-11-29 02:30:47.499445 (об'єкт datetime)
#
# value="2024-11-29 02:30:47.499445"
#
# value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
# print(value)


# def get_next_id(session, model):
#     """
#     нумерація документів у рамках кожної model
#     наступний(вілбний) id для model"""
#     max_id = session.query(func.max(model.id)).scalar()
#     return (max_id or 1)


# Функція для додавання BOM
# Шлях до папки з CSV файлами
# folder_path = r"D:\GIT\3k1s\Project\worck\finmanager\default_csv"

# Функція для додавання BOM
# def convert_csv_to_utf8_sig(file_path):
#     # Створення нового імені файлу
#     base_name, ext = os.path.splitext(file_path)
#     output_path = f"{base_name}{ext}"  # Додати суфікс '_bom'
#
#     # Читання існуючого CSV
#     with open(file_path, 'r', encoding='utf-8') as infile:
#         reader = csv.reader(infile)
#         data = list(reader)  # Читання всіх рядків
#
#     # Запис нового файлу з BOM
#     with open(output_path, 'w', encoding='utf-8-sig', newline='') as outfile:
#         writer = csv.writer(outfile)
#         writer.writerows(data)
#     print(f"Файл збережено: {output_path}")
#
# # Перебір файлів у папці
# for file_name in os.listdir(folder_path):
#     if file_name.endswith(".csv"):  # Перевірка на формат CSV
#         full_path = os.path.join(folder_path, file_name)
#         convert_csv_to_utf8_sig(full_path)
#
# print("Всі файли успішно конвертовані!")

def list_name_in_table(in_model):
    """
    list all name
    :param in_model:
    :return:
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()
    descendants = session.query(in_model).filter(in_model.name != "").all()
    session.close()
    list = [name.name for name in descendants]
    return list

def get_document_types():
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        # Выполняем запрос для получения всех типов документов
        document_types = session.query(model.DocumentType.id, model.DocumentType.name).all()

        # Разделяем результат на два списка: ids и names
        ids, names = zip(*document_types) if document_types else ([], [])

        return list(ids), list(names)
    finally:
        session.close()