from functools import wraps
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime

def unique_name(func):
    @wraps(func)
    def wrapper(instance, session, *args, **kwargs):
        # Перевірка унікальності name
        existing_record = session.query(instance.__class__).filter_by(name=instance.name).first()
        if existing_record and existing_record.id != instance.id:
            raise ValueError(f"Запис з name='{instance.name}' вже існує.")
        return func(instance, session, *args, **kwargs)

    return wrapper



    """
    Decorator for automatically saving change history of records in database tables.

    @add_version_record(session)
    def save(self):
        # Логіка збереження запису
        pass

    All tables must include the fields `previous_id`, `next_id`, and `origin_id`, which are used to track
    the version history of each record. This decorator functions as follows:

    1. **Creating a Record Copy**:
       - When a record is edited, a copy of the current record is created to preserve the current data.
       - The copy’s `previous_id` is set to the `previous_id` of the current record (if it exists).
       - The copy’s `next_id` points to the current record (the one being edited).
       - The copy’s `origin_id` remains the same as the current record's `origin_id`.

    2. **Updating the Previous Record**:
       - If the current record already has a `previous_id`, the `next_id` of that previous record is updated to point to the new copy.

    3. **Updating the Current Record Fields**:
       - The `previous_id` of the current record is updated to point to the new copy.
       - The `next_id` of the current record is set to `None`, as it is now the last record in the version chain.
       - For a new record, `origin_id` is set to its own `id`, with `previous_id` and `next_id` both set to `None`.

    This decorator enables version tracking for each record, maintaining a linked history chain that functions like a stack or queue.
    """

def add_version_record(func):
    @wraps(func)
    def wrapper(self, session, *args, **kwargs):
        if self.id:  # Якщо це існуючий запис
            # Створення копії поточного запису
            history_copy = self.__class__(**{
                column.name: getattr(self, column.name)
                for column in self.__table__.columns
                if column.name not in ('id', 'previous_id', 'next_id')
            })
            history_copy.previous_id = self.previous_id
            history_copy.next_id = self.id
            history_copy.origin_id = self.origin_id or self.id

            # Оновлення next_id для попереднього запису, якщо він існує
            if history_copy.previous_id:
                prev_record = session.query(self.__class__).get(history_copy.previous_id)
                prev_record.next_id = history_copy.id
                session.add(prev_record)

            # Оновлення поточного запису
            self.previous_id = history_copy.id
            self.next_id = None
            self.edited_date = datetime.utcnow()

            # Додавання копії для історії
            session.add(history_copy)

        else:  # Новий запис
            self.origin_id = self.id or None
            self.previous_id = None
            self.next_id = None

        # Виклик оригінальної функції
        result = func(self, session, *args, **kwargs)
        session.commit()
        return result

    return wrapper



