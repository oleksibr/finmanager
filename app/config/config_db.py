import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base
import json


class DatabasesConfig:
    def __init__(self, config_file="..//config/config.json", idx_db=None):
        self.config_file = config_file
        self.list_db = None
        self.current_db_idx = idx_db
        self.path_db = None
        self.work_dir = None
        with open(self.config_file, "r", encoding="utf-8-sig") as f:
            config_data = json.load(f)
            self.work_dir = config_data.get("dir_db")

            if os.path.isdir(self.work_dir) == None:
                try:
                    os.makedirs(self.work_dir)
                except Exception as e:
                    print(f"Не вдалося створити каталог:{self.work_dir} {e}")
                return None

        self.load_list_db()

    def load_list_db(self):
        with open(self.config_file, "r", encoding="utf-8-sig") as f:
            config_data = json.load(f)

            self.list_db = config_data.get("list_db", [])
            # TODO ??? crate DB if len(self.list_db) == 0

            self.current_db_idx = int(config_data.get("current_db", 0))

            if 0 <= self.current_db_idx < len(self.list_db):

                self.path_db = os.path.join(self.list_db[self.current_db_idx]["db_dir"],
                                            self.list_db[self.current_db_idx]["db_name"].strip("/"))
            else:
                print("Некоректний індекс поточної БД або список 'list_db' порожній.")

    def get_list_db(self):
        return self.list_db

    def get_path_db(self):
        return self.path_db

    def get_idx_db_0(self):
        return self.current_db_idx

    def get_csv_dir(self):
        with open(self.config_file, "r", encoding="utf-8-sig") as f:
            config_data = json.load(f)
            return config_data.get("default_csv_dir")

    def load_config(self):
        with open(self.config_file, "r", encoding="utf-8-sig") as f:
            config_data = json.load(f)
            current_db_index = int(config_data.get("current_db", 0))
            # db = config_data["list_db"][current_db_index]
            db_list = config_data.get("list_db", [])
            if 0 <= current_db_index < len(db_list):
                db = db_list[current_db_index]
                print(f"Поточна база даних: {db}")
            else:
                print("Некоректний індекс поточної БД або список 'list_db' порожній.")

            self.db_name = db["db_name"]
            self.db_path = os.path.join(db["db_dir"], db["db_name"].strip("/"))

    def save_config(self):
        config_data = {"db_path": self.db_path}
        {"idx_db_0": self.current_db_idx}
        {self.current_db_idx}
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)

    def set_current_db_idx(self, idx):
        with open(self.config_file, "r", encoding="utf-8-sig") as file:
            config = json.load(file)
            if "current_db" not in config:
                config["current_db"] = idx
            config["current_db"] = idx
        with open(self.config_file, "w", encoding="utf-8") as file:
            json.dump(config, file, ensure_ascii=False, indent=4)

    def add_db_in_db_list(self, name_db_file, db_dir):
        new_db_entry = {
            "db_name": name_db_file,
            "db_dir": db_dir
        }
        with open(self.config_file, "r", encoding="utf-8-sig") as file:
            config = json.load(file)

        if "list_db" not in config:
            config["list_db"] = []

        if "current_db" not in config:
            config["current_db"] = 0
        else:
            config["current_db"] = len(self.get_list_db())

        if new_db_entry not in config["list_db"]:
            config["list_db"].append(new_db_entry)

        with open(self.config_file, "w", encoding="utf-8") as file:
            json.dump(config, file, ensure_ascii=False, indent=4)

    def create_new_db(self, db_name, admin=None, pass_admin=None):

        if not db_name:
            raise ValueError("Ім'я бази даних не повинно бути порожнім")

        if not db_name.lower().endswith(('.db', '.sqlite')):
            db_name = f"{db_name}.db"

        if os.path.isdir(self.work_dir) == None:
            try:
                os.makedirs(self.work_dir)
            except Exception as e:
                print(f"Не вдалося створити каталог:{self.work_dir} {e}")
            return None

        db_url = f'sqlite:///{self.work_dir}\\{db_name}'
        try:
            engine = create_engine(db_url, echo=True)
        except Exception as e:
            print(f"Помилка при створенні бази даних '{db_url}': {e}")
            return None

        Base.metadata.create_all(engine)
        # path = engine.url.database

        conf = DatabasesConfig()
        conf.add_db_in_db_list(db_name, self.work_dir)

        return engine

    def get_cur_db_name(self):
        pass

    def get_db_engine(self):

        db_file = self.path_db

        db_exists = os.path.exists(f"{db_file}")

        if not db_exists:
            raise FileNotFoundError(f"'{db_file}' не існує.")

        db_url = f'sqlite:///{db_file}'
        engine = create_engine(db_url, echo=True)
        # Base.metadata.create_all(engine)

        return engine

    def create_session(self):

        Session = sessionmaker(bind=self.get_db_engine())
        return Session()


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
        # TODO # ??? щось повернути або підключити

    except Exception as e:
        # TODO ??? що робити коли копія не створена
        pass
