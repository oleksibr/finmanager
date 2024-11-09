import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base


def create_db_engine(db_name):
    path_db_dir = 'D:\\GIT\\3k1s\\Project\\worck\\finmanager'
    if not db_name:
        raise ValueError("Ім'я бази даних не повинно бути порожнім")

    db_url = f'sqlite:///{path_db_dir}\\finmanager_{db_name}.db'

    if os.path.isdir(path_db_dir):
        print("Каталог path_dir існує.")
    else:
        # TODO create dir
        print("Каталог path_dir не існує.")

    try:
        engine = create_engine(db_url, echo=True)
    except Exception as e:
        print(f"Помилка при створенні бази даних '{db_url}': {e}")
        return None

    Base.metadata.create_all(engine)
    path = engine.url.database
    print(f"Шлях до бази даних: {path}")

    return engine


def get_db_engine(db_name):
    db_file = f'{db_name}.db'

    db_exists = os.path.exists(db_file)

    if not db_exists:
        raise FileNotFoundError(f"'{db_file}' не існує.")

    db_url = f'sqlite:///{db_file}'
    engine = create_engine(db_url, echo=True)

    return engine


def delete_db_engine(db_name):
    db_file = f'{db_name}.db'

    # Перевіряємо, чи існує файл бази даних
    if not os.path.exists(db_file):
        raise FileNotFoundError(f"База даних '{db_file}' не існує.")

    try:
        # Видаляємо файл бази даних
        os.remove(db_file)
        print(f"База даних '{db_file}' успішно видалена.")
    except Exception as e:
        # Обробка можливих помилок при видаленні
        print(f"Помилка при видаленні бази даних '{db_file}': {e}")



def create_from_template(template_db_name, new_db_name):
    template_db_file = f'{template_db_name}.db'
    new_db_file = f'{new_db_name}.db'

    if not os.path.exists(template_db_file):
        raise FileNotFoundError(f"Шаблон бази даних '{template_db_file}' не існує.")

    # раптом база даних вже існує
    if os.path.exists(new_db_file):
        raise FileExistsError(f"Така база даних '{new_db_file}' вже існує.")

    try:
        shutil.copy(template_db_file, new_db_file)
        #TODO # ??? щось повернути або підключити

    except Exception as e:
        #TODO ??? що робити коли копія не створена
        pass


def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

