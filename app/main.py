from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from config.config_db import create_db_engine
from models.models import Level, Base


def main(msg):
    db_name = 'test_db_engine'
    try:
        engine = create_db_engine(db_name)
        engine.connect()
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Помилка при створенні бази даних '{db_name}': {e}")
        return None

    Session = sessionmaker(bind=engine)
    session = Session()

    new_level = Level(access_level=1, name='Admin', session=session)
    session.add(new_level)
    session.commit()

    try:
        new_level = Level(access_level=1, name='Admin', session=session)
        new_level.add_level(session)
    except ValueError as e:
        print(e)  # Показуємо помилку, але програма продовжує виконуватись
    except IntegrityError:
        session.rollback()
        print("Помилка з унікальним значенням у базі, але виконання продовжується")


if __name__ == '__main__':
    main('test')
