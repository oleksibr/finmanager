from functools import wraps
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime

def unique_name(func):
    @wraps(func)
    def wrapper(instance, session, *args, **kwargs):
        # Перевірка унікальності name
        existing_record = session.query(instance.__class__).filter_by(name=instance.name).first()
        if existing_record:
            raise ValueError(f"Запис з name='{instance.name}' вже існує.")
        return func(instance, session, *args, **kwargs)

    return wrapper



def add_version_record(session):
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

    def decorator(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            if instance.id:  # if it is an existing record
                # Create a copy of the current record
                history_copy = instance.__class__(**{column.name: getattr(instance, column.name)
                                                     for column in instance.__table__.columns
                                                     if column.name not in ('id', 'previous_id', 'next_id')})
                history_copy.previous_id = instance.previous_id
                history_copy.next_id = instance.id
                history_copy.origin_id = instance.origin_id or instance.id

                # renew `next_id` for pre-entry if it exists
                if history_copy.previous_id:
                    prev_record = session.query(instance.__class__).get(history_copy.previous_id)
                    prev_record.next_id = history_copy.id
                    session.add(prev_record)

                # Update the current record: `previous_id` points to a new copy, `next_id` = None
                instance.previous_id = history_copy.id
                instance.next_id = None
                instance.edited_date = datetime.utcnow()

                # Attach copy for history to session
                session.add(history_copy)

            else:  # new record
                instance.origin_id = instance.id or None
                instance.previous_id = None
                instance.next_id = None

            # We call the original function
            result = func(instance, *args, **kwargs)
            session.commit()
            return result

        return wrapper

    return decorator
