from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# from config.config_db import create_new_db, get_db_engine, create_from_template
from models.models import User, AccessLevel, Base
import config.config_db as conf_db

def main(msg):

    db_name = 'test_db_engine'
    config = conf_db.DatabasesConfig()
    engine = config.create_new_db(db_name)
    return
    try:
        engine = config.create_new_db(db_name)
        # engine.connect()
        # Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Помилка при створенні бази даних '{db_name}': {e}")
        return None

    Session = sessionmaker(bind=engine)
    session = Session()

    new_level = AccessLevel(access_level=1, name='Admin', session=session)
    session.add(new_level)
    session.commit()

    try:
        new_level = AccessLevel(access_level=1, name='Admin', session=session)
        new_level.add_level(session)
    except ValueError as e:
        print(e)  # Показуємо помилку, але програма продовжує виконуватись
    except IntegrityError:
        session.rollback()
        print("Помилка з унікальним значенням у базі, але виконання продовжується")

# Створення записів
#     root = SubcountoType(short_name='root', full_name='Root Type', pseudonym=None)
#     dir_type = SubcountoType(short_name='dir', full_name='Directory Type', pseudonym=None)
#     end_point = SubcountoType(short_name='end_point', full_name='End Point Type', pseudonym=None)
#
#     # Додавання записів до сесії
#     session.add_all([root, dir_type, end_point])
#
#     # Збереження в базі
#     session.commit()

if __name__ == '__main__':
    main('test')

