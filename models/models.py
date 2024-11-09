from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, validates, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from functools import wraps
from sqlalchemy.exc import IntegrityError

from .decorators import unique_name


from models.decorators import add_version_record

# engine = create_engine('sqlite:///example.db')

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=True, default=None)
    level_id = Column(Integer, ForeignKey('levels.id'), nullable=False, default=1)
    status = Column(Integer, nullable=True, default=0)


    def __init__(self, name, password, level_id, session):
        existing_record = session.query(User).filter_by(name=name).first()
        if existing_record:
            raise ValueError(f"Record with name='{name}' already exists.")
        self.name = name
        self.password = password
        self.level_id = level_id

@unique_name
def save_user(user, session):
    """
        level_id = 1 - system
        level_id = 2 - admin
        level_id = 3 - read_only_user
        level_id = 7 - default_level
        level_id = 8 - deleted


        Створення нового користувача
        new_user = User(name="example_user", password="secret", level_id=1)

        try:
            save_user(new_user, session)
        except ValueError as e:
            print(e)
        """
    session.add(user)
    session.commit()


def edite_user(user, session):
    # TODO
    # пам'ятати про контроль unique name
    pass


def delite_user(user, session):
    # TODO
    pass


class Level(Base):
    """
    Global config

    admin = 1 - full
    user = 2 - read-write
    guest = 3 - only view
    """
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True)
    access_level = Column(Integer, nullable=False, default=0)
    name = Column(String, nullable=False, unique=True)

    def __init__(self, access_level, name, session):
        existing_record = session.query(Level).filter_by(name=name).first()
        if existing_record:
            raise ValueError(f"Record with name='{name}' already exists.")

        self.access_level = access_level
        self.name = name

    def add_level(access_level, name, session):
        new_level = Level(access_level=access_level, name=name)
        try:
            session.add(new_level)
            session.commit()
            print(f"Level '{name}' додано успішно.")
        except IntegrityError:
            session.rollback()
            print(f"Помилка: Запис з name='{name}' вже існує.")

    def edit_level(level_id, new_access_level, new_name, session):
        level = session.query(Level).filter_by(id=level_id).first()
        if level:
            level.access_level = new_access_level
            level.name = new_name
            try:
                session.commit()
                print(f"Level з id={level_id} успішно оновлено.")
            except IntegrityError:
                session.rollback()
                print(f"Помилка: Запис з name='{new_name}' вже існує.")
        else:
            print(f"Рівень з id={level_id} не знайдено.")

    def delete_level(level_id, session):
        level = session.query(Level).filter_by(id=level_id).first()
        if level:
            session.delete(level)
            session.commit()
            print(f"Level з id={level_id} успішно видалено.")
        else:
            print(f"Рівень з id={level_id} не знайдено.")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    comments = Column(String, nullable=False, default='')
    old_comments = Column(String, nullable=True, default=None)


class EnabledTransaction(Base):
    """
    Global config + User config

    enabled id Dt-Kt to use in transaction"""
    __tablename__ = 'enabled_transaction'
    id = Column(Integer, primary_key=True)
    Dt = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    Kt = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    name = Column(String, nullable=True)


class AssociatedAccount(Base):
    """
    Global config + User config

    enabled transaction between 2 Account"""
    __tablename__ = 'associated_account'
    id = Column(Integer, primary_key=True)
    root_Dt = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    root_Kt = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    name = Column(String, nullable=True)



class DocumentType(Base):
    """
    Global config + User config
    user_type based on Global type - only new name added
    """
    __tablename__ = 'doc_types'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    user_type = Column(Integer, ForeignKey('doc_types'), nullable=True)
#TODO status???

class Status(Base):
    """ Global config
    отражает стан доумента:
    проведен spending = 1,
    не проведен spending = 0,
    видалити у корзину ,
    видален,
    черновик draft = 3
    потрібно перепровести
    потрібно скасувати проведення
    потрібно видалити
    ...
    та інші
    """
    __tablename__ = 'statuses'
    id = Column(Integer, primary_key=True)
    idx = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)


class QrCode(Base):
    __tablename__ = 'qr_codes'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)


class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, autoincrement=True, nullable=False)
    type_id = Column(Integer, ForeignKey('doc_types.id'), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=True, default=1)
    edited_date = Column(DateTime, default=datetime.utcnow)
    editor_id = Column(Integer, ForeignKey('users.id'), nullable=True, default=1)

    summ_dt = Column(Integer, nullable=True)
    summ_kt = Column(Integer, nullable=True)

    lock = Column(Integer, nullable=False, default=0)
    income_qr_code = Column(Integer, ForeignKey('qr_codes.id'), nullable=True, default=None)

    status = Column(Integer, ForeignKey('users.id'), nullable=True, default=1)

    creator = relationship("User", backref="created_documents", foreign_keys=[creator_id])
    editor = relationship("User", backref="edited_documents", foreign_keys=[editor_id])


class Operation(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False) #TODO auto or not
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    edited_date = Column(DateTime, default=datetime.utcnow)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    document = relationship("Document", backref="operations", foreign_keys=[document_id])
    creator = relationship("User", backref="created_operations", foreign_keys=[creator_id])


class TransactionType(Base):
    __tablename__ = 'transaction_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pass


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    edited_date = Column(DateTime, default=datetime.utcnow)
    dt_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    kt_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    price = Column(Integer, default=0)
    quantity = Column(Integer, default=1)
    summ = Column(Float, default=0.0)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=True)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status_id = Column(Integer, ForeignKey('statuses.id'), nullable=False, default=1)
    type = Column(Integer, ForeignKey('transaction_types.id'), nullable=False, default=1)


class AccountType(Base):
    __tablename__ = 'account_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pass


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    number = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey('account_types.id'))
    status_id = Column(Integer, ForeignKey('statuses.id'))
    lock_id = Column(Integer, ForeignKey('statuses.id'))

    edited_date = Column(DateTime, default=datetime.utcnow)

    origin_id = Column(Integer, ForeignKey('accounts.id'), nullable=True, default=None)
    previous_id = Column(Integer, ForeignKey('accounts.id'), nullable=True, default=None)
    next_id = Column(Integer, ForeignKey('accounts.id'), nullable=True, default=None)

    origin = relationship("Account", remote_side=[id], foreign_keys=[origin_id], uselist=False)
    previous = relationship("Account", remote_side=[id], foreign_keys=[previous_id], uselist=False)
    next = relationship("Account", remote_side=[id], foreign_keys=[next_id], uselist=False)

    def __repr__(self):
        parent_name = f"'{self.parent.name}'" if self.parent_id else "None"
        return f"<Account(number={self.number}, name={self.name}, parent_name={parent_name})>"

    @validates('parent_id')
    def validate_parent_account(self, key, parent_account_id):
        if parent_account_id == self.id:
            raise ValueError("Account cannot reference its own ID.")
        return parent_account_id

    @add_version_record  # Decorator for saving versions
    def save(self, session):
        """Saves changes or new account to database."""
        session.add(self)
        session.commit()

    def add_account(session, number, name, type_id, status_id, lock_id, parent_id=None):
        """Adds a new account to the database."""
        new_account = Account(
            number=number,
            name=name,
            type_id=type_id,
            status_id=status_id,
            lock_id=lock_id,
            parent_id=parent_id
        )

        try:
            new_account.save(session)  # Викликаємо метод save з декоратором
            print(f"Account '{name}' added successfully.")
        except IntegrityError as e:
            session.rollback()
            print(f"Error: Could not add account '{name}'. {e}")
        except ValueError as e:
            session.rollback()
            print(f"Validation Error: {e}")

class AccountBalance(Base):
    __tablename__ = 'account_balance'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    balance = Column(Integer, default=0.0)

    account = relationship("Account", backref="balances")
    currency = relationship("Currency")


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    code = Column(String(3), unique=True)  # e.g., 'USD', 'EUR'
    name = Column(String)

