import os
import csv
from datetime import datetime

from sqlalchemy import func, text, inspect
from sqlalchemy.exc import IntegrityError
# from models.models import Level, Account, AccountType, AssociatedAccount, Base
import app.config.config_db as conf_db
import app.models.models as model
from app.models.models import User, AccessLevel, Comment, AssociatedAccount, DocumentType, Status, QrCode, Document, \
    Operation, Transaction, AccountType, Unit, SubcountoBalance, ScTransactionType, ScTransaction, SubcountoType, \
    Subcounto, HistoryAccount, Account, AccountBalance, Currency


# root_dt_values = model.AssociatedAccount.find_all_record_kt(session, 30)
# root_kt_values = model.AssociatedAccount.find_all_record_dt(session, 30)
# UI

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


# list_parent(model.Subcounto, 1)
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
        "SubcountoBalance": model.SubcountoBalance,
        "SubcountoType": model.SubcountoType,
        "Subcounto": model.Subcounto,
        "TransactionType": model.TransactionType,
        "Transaction": model.Transaction,
        "Unit": model.Unit,
        "User": model.User
    }
    return table_classes_name


# GUI
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
    nn = config.get_list_db()
    return [val["db_name"] for val in config.get_list_db()]


# ddd = conf_db.DatabasesConfig()
# ddd.set_current_db_idx(5)


# print(get_list_db())
# print(len(get_list_db()))

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


# Ui
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


# ddd = {'id': 5, 'name': "user1", 'level_id': 1}
# con = conf_db.DatabasesConfig()
# sss = con.create_session()
# add(sss, model.User, **ddd)
# sss.commit()
# sss.close()


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


# TODO
def edite_access_level(new_name=None, new_level=None, id=None, user=None):
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


# # create_default_db("test")
# create_default_db()

# delete_all_row_reset_id("AssociatedAccount")
# add_data_from_single_csv("..\default_csv\AssociatedAccount.csv")

# edite_access_level("admin","r","admin")
#
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

# Отримати поля таблиці
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

"""Початок CRUD функцій"""


def create_user(name, password, status=None):
    """
    Create a new User in the database.
    :param name: User name (str)
    :param password: User password (str)
    :param status: User status (str), default is None
    :return: The created User instance
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        # Assign default level_id for new users as 'viewer' (level_id = 3)
        access_level = session.query(model.AccessLevel).filter(model.AccessLevel.name.in_(['viewer', 'viever'])).first()
        if not access_level:
            raise ValueError("Access level 'viewer' or 'viever' not found in the database.")

        new_user = model.User(session=session, name=name, password=password, level_id=access_level.id, status=status)
        session.add(new_user)
        session.commit()
        print(f"User '{name}' created successfully.")
        return new_user
    except IntegrityError as e:
        session.rollback()
        print(f"Error: Could not create user '{name}'. {e}")
    except ValueError as e:
        session.rollback()
        print(f"Validation Error: {e}")
    finally:
        session.close()


# create_user("test_user1", "password1", status="enable")
# create_user("test_user2", "password2", status="enable")


def get_user_by_id(user_id):
    """
    Retrieve a User by creation number from the database.
    :param user_id: User creation number (int)
    :return: The User instance if found, otherwise None
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        users = session.query(model.User).order_by(model.User.id).all()
        if user_id <= 0 or user_id > len(users):
            print(f"User with creation number {user_id} not found.")
            return None

        user = users[user_id - 1]
        print(f"User found: {user.name}, Level ID: {user.level_id}")
        return user
    finally:
        session.close()


# get_user_by_id(2)


def get_all_users():
    """
    Retrieve all Users from the database.
    :return: List of User instances
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        users = session.query(model.User).all()
        for user in users:
            access_level = session.get(model.AccessLevel, user.level_id)
            level_name = access_level.name if access_level else "Unknown"
            print(f"User ID: {user.id}, Name: {user.name}, Level: {level_name}")
        return users
    finally:
        session.close()


# get_all_users()

# Зміна пароль на логіну

# def update_user(user_id, **kwargs):
#     """
#     Update a User in the database.
#     :param user_id: User ID (int)
#     :param kwargs: Fields to update (e.g., name='new_name', password='new_password')
#     :return: The updated User instance
#     """
#     config = conf_db.DatabasesConfig()
#     engine = config.get_db_engine()
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     try:
#         user = session.get(model.User, user_id)
#         if not user:
#             print(f"User with ID {user_id} not found.")
#             return None
#
#         for key, value in kwargs.items():
#             if hasattr(user, key):
#                 setattr(user, key, value)
#             else:
#                 raise ValueError(f"Attribute '{key}' does not exist in User.")
#
#         session.commit()
#         print(f"User '{user.name}' updated successfully.")
#         return user
#     except ValueError as e:
#         session.rollback()
#         print(f"Validation Error: {e}")
#     finally:
#         session.close()
#
# update_user(2, name="updated_user2", password="new_password2")


def delete_user(user_id):
    """
    Delete a User from the database by ID.
    :param user_id: User ID (int)
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        user = session.get(model.User, user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return

        # Ensure that only users with appropriate level can be deleted
        access_level = session.get(model.AccessLevel, user.level_id)
        if access_level and access_level.level == 'a':
            print("System user cannot be deleted.")
            return

        session.delete(user)
        session.commit()
        print(f"User with ID {user_id} deleted successfully.")
    finally:
        session.close()


# delete_user(5)
# get_user_by_id(5)


def get_accounts_by_parent_id(parent_id):
    """
    Retrieve accounts from the database by parent ID.
    :param parent_id: Parent ID to filter accounts (int)
    :return: List of Account instances if found, otherwise empty list
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        accounts = session.query(model.Account).filter(model.Account.parent_id == parent_id).all()
        if accounts:
            for account in accounts:
                print(f"Account ID: {account.id}, Name: {account.name}, Parent ID: {account.parent_id}")
        else:
            print(f"No accounts found with parent_id {parent_id}.")
        return accounts
    finally:
        session.close()


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


# ids, names = get_document_types()
# print(ids)   # Список id
# print(names) # Список name


# TODO: Функції сет статус (иф нон в айді в моделі делає нову строчку пусту а в параметрах) і гет статус,
# #Гет статус: модель, айді(по умолчанию нон), статус(драфт - 1) - Done.


def create_empty_document():
    """
    Создает новый пустой документ с предварительным статусом 'draft'.
    Возвращает созданный документ.
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        # Устанавливаем статус draft (предполагаем, что его ID равно 1)
        draft_status_id = 1

        # Создаем новый документ со статусом 'draft'
        new_document = model.Document(
            number=-1,
            type_id=-1,
            date=datetime.utcnow(),
            status=draft_status_id
        )

        session.add(new_document)
        session.commit()
        print(f"Создан пустой документ с ID: {new_document.id}")

        return new_document
    except IntegrityError as e:
        session.rollback()
        print(f"Ошибка: Не удалось создать пустой документ. {e}")
    finally:
        session.close()


# create_empty_document()


def get_document_status(document_id=None):
    """
    Получает статус документа по его ID. Если ID не указан, возвращается статус документа с ID = 1.
    :param document_id: ID документа (int)
    :return: Статус документа (str)
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        if document_id:
            document = session.get(model.Document, document_id)
        else:
            document = session.get(model.Document, 1)  # По умолчанию берём ID 1

        if document:
            status = session.get(model.Status, document.status)
            print(f"Статус документа с ID {document_id}: {status.name}")
            return status.name
        else:
            print(f"Документ с ID {document_id} не найден.")
            return None
    finally:
        session.close()


def set_document_status(document_id=None, status_id=None):
    """
    Устанавливает статус документа. Если документ не найден по ID, создаёт новый документ с указанным статусом.
    :param document_id: ID документа (int), по умолчанию None
    :param status_id: Новый статус документа (int), обязателен
    :return: Обновленный или созданный документ
    """
    if status_id is None:
        print("Ошибка: статус должен быть указан.")
        return None

    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        if document_id:
            # Пытаемся найти документ по ID
            document = session.get(model.Document, document_id)
            if document:
                document.status = status_id
                print(f"Статус документа с ID {document_id} успешно обновлён на {status_id}.")
            else:
                # Если документа с таким ID нет, создаём новый
                print(f"Документ с ID {document_id} не найден. Создаем новый документ.")
                document = model.Document(
                    number=-1,
                    type_id=-1,
                    date=datetime.utcnow(),
                    status=status_id
                )
                session.add(document)
        else:
            # Создаём новый документ, если ID не указан
            document = model.Document(
                number=-1,
                type_id=-1,
                date=datetime.utcnow(),
                status=status_id
            )
            session.add(document)

        session.commit()
        return document
    except IntegrityError as e:
        session.rollback()
        print(f"Ошибка: не удалось установить статус документа. {e}")
    finally:
        session.close()


"""CRUD Transaction"""


def new_transaction(
                    operation_id,
                    date,
                    edited_date,
                    price,
                    quantity,
                    summ,
                    decimal_point_price,
                    decimal_point_quantity,
                    dt_id,
                    dt_sc_id,
                    kt_id,
                    kt_sc_id,
                    currency_id,
                    comment_id,
                    creator_id,
                    status_id,
                    type):
    """
    Creates a new transaction record in the database.

    :param operation_id: parent operation ID to which this transaction is linked.
    :param date: Date of the transaction.
    :param edited_date: Date when the transaction was edited.
    :param price: Price of the transaction.
    :param quantity: Quantity involved in the transaction.
    :param summ: Sum value of the transaction.
    :param decimal_point_price: Decimal precision for the price.
    :param decimal_point_quantity: Decimal precision for the quantity.
    :param dt_id: Debit account ID.
    :param dt_sc_id: Debit subaccount ID.
    :param kt_id: Credit account ID.
    :param kt_sc_id: Credit subaccount ID.
    :param currency_id: ID of the currency used in the transaction.
    :param comment_id: ID of the comment associated with the transaction.
    :param creator_id: User ID who created the transaction.
    :param status_id: Status ID of the transaction.
    :param type: Type of the transaction.

    :return: Newly created transaction object.
    """

    # Database Configuration Setup
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    # transaction_values = \
    #     {
    #         'operation_id': 1,
    #         'status': 'edited',
    #         'price': 100.25,
    #         'quantity': 5.5,
    #         'summ': 550.25,
    #         'decimal_point_price': 2,
    #         'decimal_point_quantity': 4,
    #         'dt_id': 1,
    #         'dt_sc_id': 2,
    #         'kt_id': 3,
    #         'kt_sc_id': 4,
    #         'currency_id': 1,
    #         'comment_id': 10,
    #         'creator_id': 1,
    #         'status_id': 1,
    #         'type': 1
    #     }

    transaction_values = {}

    try:

        # Проверяем наличие родительской операции
        if not session.query(model.Operation).filter_by(id=operation_id).first():
            raise ValueError("Parent operation ID must exist in the database.")

        # Обработка поля date
        # if (session.query(model.Operation).filter_by(id=operation_id).first()).document_id:
        #     doc_id = (session.query(model.Operation).filter_by(id=operation_id).first()).document_id
        #     if not session.query(model.Document).filter_by(id=doc_id).first():
        #         raise ValueError("Parent operation ID must exist in the database.")
        #     transaction_values['date'] = date if date else datetime.utcnow()
        transaction_values['date'] = date if date else datetime.utcnow()

        # Обработка поля edited_date
        transaction_values['edited_date'] = edited_date if edited_date else None

        # Обработка поля price
        if price != 0:
            transaction_values['price'] = int(float(price) * 10 ** decimal_point_price)

        # Обработка поля quantity
        if quantity != 0:
            transaction_values['quantity'] = int(float(quantity) * 10 ** decimal_point_quantity)

        # Обработка поля summ
        if summ != 0:
            transaction_values['summ'] = int(float(summ) * 10 ** decimal_point_price)
        else:
            raise ValueError("Sum value must be provided.")

        # Значения по умолчанию для decimal_point_price и decimal_point_quantity
        transaction_values['decimal_point_price'] = decimal_point_price
        transaction_values['decimal_point_quantity'] = decimal_point_quantity

        # Обработка dt_id и dt_sc_id
        if not session.query(model.Account).filter_by(id=dt_id).first():
            raise ValueError("Parent operation ID must exist in the database.")
        transaction_values['dt_id'] = dt_id

        if not session.query(model.Account).filter_by(id=kt_id).first():
            raise ValueError("Parent operation ID must exist in the database.")
        transaction_values['kt_id'] = kt_id

        if dt_sc_id and not session.query(model.Subcounto).filter_by(id=dt_sc_id).first():
            raise ValueError("Parent operation ID must exist in the database.")
        transaction_values['dt_sc_id'] = dt_sc_id

        if kt_sc_id and not session.query(model.Subcounto).filter_by(id=kt_sc_id).first():
            raise ValueError("Parent operation ID must exist in the database.")
        transaction_values['kt_sc_id'] = kt_sc_id


        # Обработка currency_id, comment_id, creator_id, status_id, type
        if currency_id and not session.query(model.Currency).filter_by(id=currency_id).first():
            raise ValueError("Parent operation ID must exist in the database.")
        transaction_values['currency_id'] = currency_id

        transaction_values['comment_id'] = 1 # comment_id
        transaction_values['creator_id'] = 1 # creator_id
        transaction_values['status_id'] = 2 # status_id
        transaction_values['type'] = 1 # type

        # Создание новой транзакции
        # new_transaction = model.Transaction(**transaction_values)

        # added_instance = add(session, model.Transaction, **ddd)

        added_instance = add(session, model.Transaction, **transaction_values)
        session.commit()

        print(f"Transaction with ID {added_instance.id} created successfully.")
        return added_instance

    except Exception as e:
        session.rollback()
        print(f"Error: Could not create transaction. {e}")
    finally:
        session.close()



# ddd = \
#     {
#         'operation_id': 1,
#         'date' : '',
#         'edited_date' : '',
#         'price': 100.25,
#         'quantity': 5.5,
#         'summ': 550.25,
#         'decimal_point_price': 2,
#         'decimal_point_quantity': 4,
#         'dt_id': 1,
#         'dt_sc_id': 2,
#         'kt_id': 3,
#         'kt_sc_id': 4,
#         'currency_id': 1,
#         'comment_id': 10,
#         'creator_id': 1,
#         'status_id': 1,
#         'type': 1
#     }
#

# new_transaction(**ddd)

# transaction_data = {
#     'document_id': 1,
#     'operation_id': 1,
#     'status': 'edited',
#     'price': 100.25,
#     'quantity': 5.5,
#     'summ': 550.25,
#     'decimal_point_price': 2,
#     'decimal_point_quantity': 4,
#     'dt_id': 1,
#     'dt_sc_id': 2,
#     'kt_id': 3,
#     'kt_sc_id': 4,
#     'currency_id': 1,
#     'comment_id': 10,
#     'creator_id': 1,
#     'status_id': 1,
#     'type': 1
# }
#
# new_transaction(**transaction_data)


def get_transaction_by_id(transaction_id):
    """
    Retrieve a Transaction by ID from the database.
    :param transaction_id: Transaction ID (int)
    :return: The Transaction instance if found, otherwise None
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        transaction = session.get(model.Transaction, transaction_id)
        if transaction:
            print(
                f"Transaction found: ID: {transaction.id}, Price: {transaction.price}, Quantity: {transaction.quantity}")
        else:
            print(f"Transaction with ID {transaction_id} not found.")
        return transaction
    finally:
        session.close()


# get_transaction_by_id(2)


def get_all_transactions():
    """
    Retrieve all Transactions from the database.
    :return: List of Transaction instances
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        transactions = session.query(model.Transaction).all()
        for transaction in transactions:
            print(
                f"Transaction ID: {transaction.id}, Price: {transaction.price}, Quantity: {transaction.quantity}, Sum: {transaction.summ}")
        return transactions
    finally:
        session.close()


def save_transaction(transaction_data):
    """
    Save a new Transaction to the database using a dictionary of data.
    :param transaction_data: Dictionary containing transaction data
    :return: The created Transaction instance
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        new_transaction = model.Transaction(**transaction_data)
        session.add(new_transaction)
        session.commit()
        print(f"Transaction with ID {new_transaction.id} created successfully.")
        return new_transaction
    except Exception as e:
        session.rollback()
        print(f"Error: Could not create transaction. {e}")
    finally:
        session.close()


# Пустышка для сейва транзакции

# new_transaction = save_transaction(transaction_data)
# if new_transaction:
#     print(f"Создана транзакция с ID {new_transaction.id}")


def update_transaction(transaction_id, updated_data):
    """
    Update an existing Transaction in the database.
    :param transaction_id: Transaction ID (int)
    :param updated_data: Dictionary containing fields to update
    :return: The updated Transaction instance
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        # Get transaction_id dynamically from PyQt interface
        transaction = session.get(model.Transaction, transaction_id)
        if not transaction:
            print(f"Transaction with ID {transaction_id} not found.")
            return None

        for key, value in updated_data.items():
            if hasattr(transaction, key):
                setattr(transaction, key, value)
            else:
                raise ValueError(f"Attribute '{key}' does not exist in Transaction.")

        session.commit()
        print(f"Transaction with ID {transaction.id} updated successfully.")
        return transaction
    except ValueError as e:
        session.rollback()
        print(f"Validation Error: {e}")
    finally:
        session.close()


# transaction_id = 2  # Идентификатор транзакции, который будет автоматически передан из PyQt
# updated_data = {
#     'price': 150,
#     'quantity': 10,
#     'summ': 1500,
#     'edited_date': datetime.utcnow()
# }
#
# Вызов функции обновления транзакции
# update_transaction(transaction_id, updated_data)
def delete_all_data_in_database():
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        # Удаление всех данных из всех таблиц
        session.query(Transaction).delete()
        session.query(Operation).delete()
        session.query(Document).delete()
        session.query(Comment).delete()
        session.query(AssociatedAccount).delete()
        session.query(DocumentType).delete()
        session.query(Status).delete()
        session.query(QrCode).delete()
        session.query(ScTransaction).delete()
        session.query(ScTransactionType).delete()
        session.query(SubcountoBalance).delete()
        session.query(Subcounto).delete()
        session.query(SubcountoType).delete()
        session.query(Unit).delete()
        session.query(HistoryAccount).delete()
        session.query(AccountBalance).delete()
        session.query(Account).delete()
        session.query(AccountType).delete()
        session.query(Currency).delete()
        session.query(User).delete()
        session.query(AccessLevel).delete()

        # Коммит изменений для удаления всех записей
        session.commit()
        print("All data deleted successfully.")

    except Exception as e:
        session.rollback()
        print(f"Error: Could not delete data. {e}")
    finally:
        session.close()


"""CRUD функції витяжки рахунків"""


def get_grouped_accounts():
    """
    Получает сгруппированные субсчета для каждого корневого счёта.
    :return: Список группированных субсчетов, каждый из которых представлен в виде списка
    """
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        # Query the accounts table for all accounts
        all_accounts = session.query(Account).all()

        # Create a list to store grouped subaccounts
        grouped_accounts = []

        # Create a placeholder for accounts with parent_id = 0
        root_zero_accounts = []

        # Loop through all accounts to find root accounts (those with two-digit numbers or special root numbers)
        for root_account in all_accounts:
            if root_account.parent_id == 0:
                root_zero_accounts.append(
                    [root_account.id, root_account.parent_id, root_account.number, root_account.name])
            elif (10 <= root_account.number < 99) or (10001 <= root_account.number <= 10009):
                # Find all subaccounts under the current root account
                if root_account.number < 100:
                    subaccounts = [
                        account for account in all_accounts if str(account.number).startswith(
                            str(root_account.number)) and account.number != root_account.number
                    ]
                else:
                    subaccounts = [
                        account for account in all_accounts if str(account.number).startswith(
                            str(root_account.number)) and account.number != root_account.number
                    ]

                # Append root account and its subaccounts as a single group
                if subaccounts:
                    root_and_subaccounts = [
                        [root_account.id, root_account.parent_id, root_account.number, root_account.name]]
                    root_and_subaccounts.extend([
                        [subaccount.id, subaccount.parent_id, subaccount.number, subaccount.name] for subaccount in
                        subaccounts
                    ])
                    grouped_accounts.append(root_and_subaccounts)

        # Add the root_zero_accounts as an empty column before the main grouped accounts
        if root_zero_accounts:
            grouped_accounts.insert(0, root_zero_accounts)

        return grouped_accounts
    except Exception as e:
        print(f"Ошибка: не удалось получить сгруппированные счета. {e}")
    finally:
        session.close()


# Usage
grouped_accounts = get_grouped_accounts()

# Print grouped accounts, ensuring that each root is followed by its subaccounts
for group in grouped_accounts:
    for account in group:
        print(account)
    print("\n")

# def get_grouped_accounts():
#     """
#     Получает сгруппированные субсчета для каждого корневого счёта.
#     :return: Список группированных субсчетов, каждый из которых представлен в виде списка
#     """
#     config = conf_db.DatabasesConfig()
#     session = config.create_session()
#
#     try:
#         # Query the accounts table for all accounts
#         all_accounts = session.query(Account).all()
#
#         # Create a list to store grouped subaccounts
#         grouped_accounts = []
#
#         # Loop through all accounts to find root accounts (those with two-digit numbers or special root numbers)
#         for root_account in all_accounts:
#             if (10 <= root_account.number < 99) or (10001 <= root_account.number <= 10009):
#                 # Find all subaccounts under the current root account
#                 if root_account.number < 100:
#                     subaccounts = [
#                         account for account in all_accounts if str(account.number).startswith(
#                             str(root_account.number)) and account.number != root_account.number
#                     ]
#                 else:
#                     subaccounts = [
#                         account for account in all_accounts if str(account.number).startswith(
#                             str(root_account.number)) and account.number != root_account.number
#                     ]
#
#                 # Append root account information only if subaccounts exist
#                 if subaccounts:
#                     grouped_accounts.append(
#                         [root_account.id, root_account.parent_id, root_account.number, root_account.name])
#
#                     # Append all subaccounts under the current root account
#                     for subaccount in subaccounts:
#                         grouped_accounts.append(
#                             [subaccount.id, subaccount.parent_id, subaccount.number, subaccount.name])
#
#         return grouped_accounts
#     except Exception as e:
#         print(f"Ошибка: не удалось получить сгруппированные счета. {e}")
#     finally:
#         session.close()

# Пустая колонка между нулевым и первым поставить пустую колонку,построчно собрать всю таблицу в виде масива. Однако в какойто момент нужно будет выбирать по айдишнику
# Комперхейшен
