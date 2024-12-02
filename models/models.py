from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship, validates, backref, session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from functools import wraps
from sqlalchemy.exc import IntegrityError
import finmanager.config.config_db as conf_db
# from models.decorators import unique_name, add_version_record
# from sqlalchemy.orm import declarative_base
# engine = create_engine('sqlite:///example.db')

Base = declarative_base()


class User(Base):
    """
        #         level_id = 1 - system
        #         level_id = 2 - admin
        #         level_id = 3 - read_only_user
        #         level_id = 7 - default_level
        #         level_id = 8 - deleted
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=True, default=None)
    level_id = Column(Integer, ForeignKey('access_level.id'), nullable=False)
    status = Column(Integer, nullable=True, default=0)


    def __init__(self,session,**kwargs):
        self.id = kwargs.pop('id', None)  # За замовчуванням None
        self.name = kwargs.pop('name', "John Doe")
        self.password = kwargs.pop('password', 7)
        self.level_id = kwargs.pop('level_id', 7)
        self.status = kwargs.pop('status', None)

        if self.name:
            existing_record = session.query(User).filter_by(name=self.name).first()
            if existing_record:
                raise ValueError(f"Record with name='{self.name}' already exists.")

    def edite(self, session):
        # TODO
        # пам'ятати про контроль unique name
        pass

    def delite(self, session):
        # TODO
        pass


class AccessLevel(Base):
    """
    Global config

    admin = 1 - full
    user = 2 - read-write
    guest = 3 - only view
    """
    __tablename__ = 'access_level'

    id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False, default=1)
    name = Column(String, nullable=False, unique=True)


    def __init__(self, session, **kwargs):
        self.id = kwargs.pop('id', None)  # За замовчуванням None
        self.name = kwargs.pop('name', None)
        self.level = kwargs.pop('level', None)
        if self.name:
            existing_record = session.query(AccessLevel).filter_by(name=self.name).first()
            if existing_record:
                raise ValueError(f"Record with name='{self.name}' already exists.")


    def edit_level(self, session, **kwargs):
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    raise ValueError(f"Attribute '{key}' does not exist in AccessLevel.")

            session.commit()
            print(f"AccessLevel '{self.name}' updated successfully.")
        except Exception as e:
            session.rollback()
            raise ValueError(f"Error editing AccessLevel: {e}")


    def delete_level(level_id, session):
        # level = session.query(AccessLevel).filter_by(id=level_id).first()
        # if level:
        #     session.delete(level)
        #     session.commit()
        #     print(f"Level з id={level_id} успішно видалено.")
        # else:
        #     print(f"Рівень з id={level_id} не знайдено.")
        pass


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    comments = Column(String, nullable=False, default='')
    old_comments = Column(String, nullable=True, default=None)


class AssociatedAccount(Base):
    """
    Global config + User config
    enabled transaction between 2 Account"""

    __tablename__ = 'associated_account'
    id = Column(Integer, primary_key=True)
    root_dt = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    root_kt = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    name = Column(String, nullable=True)

    @classmethod
    def find_record_dt_kt(cls, session, dt, kt):
        """
        Class method
        Search for a record with the specified dt and kt."""
        return session.query(AssociatedAccount).filter_by(root_dt=dt, root_kt=kt).first()

    @classmethod
    def find_all_record_dt(cls, session, dt):
        """
        Class method
        Search all record with the specified dt."""
        return [record.root_kt for record in session.query(AssociatedAccount).filter_by(root_dt=dt).all()]

    @classmethod
    def find_all_record_kt(cls, session, kt):
        """
        Class method
        Search all records with the specified kt."""
        return [record.root_dt for record in session.query(AssociatedAccount).filter_by(root_kt=kt).all()]



class DocumentType(Base):
    """
    Global config + User config
    user_type based on Global type - only new name added

    """
    __tablename__ = 'document_type'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)

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
    number = Column(Integer, nullable=False)
    operations = relationship("Operation", foreign_keys="[Operation.document_id]", backref="document_operations")
    user_number = Column(Integer, nullable=True)

    date = Column(DateTime, default=datetime.utcnow)
    edited_date = Column(DateTime, default=datetime.utcnow)
    summ_dt = Column(Integer, nullable=True)
    summ_kt = Column(Integer, nullable=True)
    lock = Column(Integer, nullable=False, default=0)

    type_id = Column(Integer, ForeignKey('document_type.id'), nullable=False)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    editor_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status = Column(Integer, ForeignKey('users.id'), nullable=True)
    income_qr_code = Column(Integer, ForeignKey('qr_codes.id'), nullable=True)

    creator = relationship("User", backref="created_documents", foreign_keys=[creator_id])
    editor = relationship("User", backref="edited_documents", foreign_keys=[editor_id])

    def get_doc_name(self, session):
        """
        Повертає ім'я документа на основі type_id, використовуючи DocumentType.
        config = conf_db.DatabasesConfig()
        session = config.create_session()
        document = session.query(Document).get(1)  # Отримання документа з ID 1
        doc_name = document.get_doc_name(session)
        """
        doc_type = session.query(DocumentType).filter_by(id=self.type_id).first()
        if doc_type:
            return doc_type.name
        return None  # Якщо запис не знайдено

    def save(self, session):
        """
        exemplar method
        Зберігає зміни в базі даних.
        """
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e


class Operation(Base):
    __tablename__ = 'operations'

    document_id = Column(Integer, ForeignKey('documents.id'), nullable=True)
    id = Column(Integer, primary_key=True)
    transactions = relationship("Transaction", foreign_keys="[Transaction.operation_id]", backref="operation")  # Множинний зв'язок

    number = Column(Integer, nullable=False) #TODO auto or not
    date = Column(DateTime, default=datetime.utcnow)
    edited_date = Column(DateTime, default=datetime.utcnow)

    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=True)

    # transaction = relationship("Document", backref="operations", foreign_keys="[operation_id]")
    # creator = relationship("User", backref="created_operations", foreign_keys=[creator_id])


class TransactionType(Base):
    __tablename__ = 'transaction_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)


class Transaction(Base):
    __tablename__ = 'transactions'

    operation_id = Column(Integer, ForeignKey('operations.id'), nullable=True)  # Зв'язок із Operation
    id = Column(Integer, primary_key=True)

    date = Column(DateTime, default=datetime.utcnow)
    edited_date = Column(DateTime, default=datetime.utcnow)
    price = Column(Integer, default=0)
    quantity = Column(Integer, default=1)
    summ = Column(Integer, default=0)
    decimal_point_price = Column(Integer, default=2)
    decimal_point_quantity = Column(Integer, default=4)

    dt_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    dt_sc_id = Column(Integer, ForeignKey('subcountos.id'), nullable=True)
    # dt_sc_tabel_id = Column(Integer, ForeignKey('subcounto_table.id'), nullable=True)

    kt_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    kt_sc_id = Column(Integer, ForeignKey('subcountos.id'), nullable=True)
    # kt_sc_tabel_id = Column(Integer, ForeignKey('subcounto_table.id'), nullable=True)

    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=True)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status_id = Column(Integer, ForeignKey('statuses.id'), nullable=False)
    type = Column(Integer, ForeignKey('transaction_types.id'), nullable=False)


    @property
    def summ_human(self):
        """Повертає суму в стандартному вигляді (наприклад, 123.45)."""
        return self.summ / (10 ** self.decimal_point_price) if self.summ is not None else None

    @summ_human.setter
    def summ_human(self, value):
        """Приймає суму у стандартному вигляді (наприклад, 123.45) і конвертує в мінімальні одиниці."""
        self.summ = int(value * (10 ** self.decimal_point_price))


class AccountType(Base):
    """
        id;name
        1;sys
        2;root_s
        3;dir_ss
        4;end_point
        5;hide_sys_dir
        6;hide_sys_end_point
        7;decommission
    """
    __tablename__ = 'account_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


    # @classmethod
    # def add(cls, session, **kwargs):
    #     """
    #     Додає новий документ.
    #     """
    #     new_row = AccountType(**kwargs)
    #     session.add(new_row)
    #     try:
    #         session.commit()
    #         return new_row
    #     except Exception as e:
    #         session.rollback()
    #         raise ValueError(f"Error adding document: {e}")


class Unit(Base):
    __tablename__ = 'units'
    """
    :point_type
        0 - root
        1 - subdir
        2 - end point
    """

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    point_type = Column(Integer, default=None)
    parent_id = Column(Integer, ForeignKey('units.id'), nullable=True)
    status_id = Column(Integer, ForeignKey('statuses.id'))

    # def __init__(self, session=None, **kwargs):
    #     super().__init__(**kwargs)
    #     self.session = session

    # @validates('parent_unit_id')
    # def validate_parent_unit(self, key, parent_unit_id, session):
    #     if parent_unit_id == self.id:
    #         raise ValueError("Subkonto cannot reference its own ID.")
    #     parent = parent_unit_id
    #     while parent != '0':
    #         config = conf_db.DatabasesConfig()
    #         session = config.create_session()
    #         if parent == self.id:
    #             raise ValueError("Cyclic reference detected in parent_subkonto.")
    #         parent = self.session.query(Unit).get(parent)  # .parent_unit_id
    #     return parent_unit_id

    # def validate(self, kwargs, session):
    #     if 'parent_unit_id' in kwargs:
    #         self.validate_parent_unit('parent_unit_id', kwargs['parent_unit_id'], session)
    #
    # def validate_parent_unit(self, key, parent_unit_id, session):
    #     if parent_unit_id == self.id:
    #         raise ValueError("Subkonto cannot reference its own ID.")
    #
    #     parent = parent_unit_id
    #     while parent is not None:
    #         if parent == self.id:
    #             raise ValueError("Cyclic reference detected in parent_subkonto.")
    #         parent = session.query(Unit).get(parent).parent_unit_id
    #     return parent_unit_id
    #


class SubcountoBalance(Base):
    __tablename__ = 'subcounto_balance'

    id = Column(Integer, primary_key=True)
    subcounto_id = Column(Integer, ForeignKey('subcountos.id'))
    currency_id = Column(Integer, ForeignKey('currencies.id'))

    balance = Column(Integer, default=0)
    balance_quantity = Column(Integer, default=0)
    price = Column(Integer, default=0)

    dt = Column(Integer, default=0)
    kt = Column(Integer, default=0)
    quantity_dt = Column(Integer, default=0)
    quantity_kt = Column(Integer, default=0)

    balance_dt = Column(Integer, default=0)
    balance_kt = Column(Integer, default=0)
    balance_quantity_dt= Column(Integer, default=0)
    balance_quantity_kt= Column(Integer, default=0)

    decimal_point_price = Column(Integer, default=2)
    decimal_point_quantity = Column(Integer, default=4)

    account = relationship("Subcounto", backref="balances")


class ScTransactionType(Base):
    __tablename__ = 'sc_transaction_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)


class ScTransaction(Base):
    __tablename__ = 'sc_transactions'

    id = Column(Integer, primary_key=True)
    subcounto_id = Column(Integer, ForeignKey('subcountos.id'))

    number = Column(Integer, autoincrement=True, nullable=False)
    quantity = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    dt_summ = Column(Integer, nullable=True)
    kt_summ = Column(Integer, nullable=True)
    currency = Column(Integer, ForeignKey('currencies.id'))
    decimal_point_price = Column(Integer, default=2)
    decimal_point_quantity = Column(Integer, default=4)

    sc_transactions_type = Column(Integer, ForeignKey('sc_transaction_types.id'))
    transaction_id = Column(Integer, ForeignKey("transactions.id"))

    unit = Column(Integer, ForeignKey('units.id'))  #одиниця виміру

    @property
    def summ_human(self):
        """Повертає суму в стандартному вигляді (наприклад, 123.45)."""
        return self.summ / (10 ** self.decimal_point_price) if self.summ is not None else None

    @summ_human.setter
    def summ_human(self, value):
        """Приймає суму у стандартному вигляді (наприклад, 123.45) і конвертує в мінімальні одиниці."""
        self.summ = int(value * (10 ** self.decimal_point_price))

    @property
    def quantity_human(self, value):
        """Приймає суму у стандартному вигляді (наприклад, 123.45) і конвертує в мінімальні одиниці."""
        self.summ = int(value * (10 ** self.decimal_point_quantity))

    @quantity_human.setter
    def quantity_human(self, value):
        """Приймає суму у стандартному вигляді (наприклад, 123.45) і конвертує в мінімальні одиниці."""
        self.summ = int(value * (10 ** self.decimal_point_quantity))


class SubcountoType(Base):
    """
        'root', 'dir', 'if end_point then = ['service_record', 'counted', 'services',  ...]
    """
    __tablename__ = 'subcounto_types'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    pseudonym = Column(String, nullable=True)


class Subcounto(Base):
    __tablename__ = 'subcountos'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('subcountos.id'), nullable=True)

    number = Column(Integer, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)

    type_id = Column(Integer, ForeignKey('subcounto_types.id'))  # dir or end point
    status_id = Column(Integer, ForeignKey('statuses.id'))

    sc_transactions = relationship("ScTransaction", backref="subcounto", foreign_keys=[ScTransaction.subcounto_id])

    # @validates('parent_id')
    # def validate_parent_subkonto(self, key, parent_id):
    #     if parent_id == self.id:
    #         raise ValueError("Subkonto cannot reference its own ID.")
    #     parent = parent_id
    #     while parent:
    #         if parent == self.id:
    #             raise ValueError("Cyclic reference detected in parent_subkonto.")
    #         parent = session.query(Subcounto).get(parent).parent_id
    #     return parent_id



class HistoryAccount(Base):
    __tablename__ = 'history_accounts'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    number = Column(Integer, unique=False, nullable=False)  # Дозволяємо дублювання
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type_id = Column(Integer, ForeignKey('account_types.id'))
    status_id = Column(Integer, ForeignKey('statuses.id'))
    lock_id = Column(Integer, ForeignKey('statuses.id'))
    subcounto_id = Column(Integer, ForeignKey('subcountos.id'))

    edited_date = Column(DateTime, default=datetime.utcnow)

    # def add(self, session, **kwargs):
    #     """
    #     Додає новий запис HistoryAccount.
    #     """
    #     new_row = HistoryAccount(**kwargs)
    #     session.add(new_row)
    #     try:
    #         session.commit()
    #         return new_row
    #     except Exception as e:
    #         session.rollback()
    #         raise ValueError(f"Error adding HistoryAccount: {e}")


class Account(Base):
    """
   type_id: account_types.id(id;name)
        1;sys
        2;root_s
        3;dir_ss
        4;end_point
        5;hide_sys_dir
        6;hide_sys_end_point
        7;decommission

    status_id: statuses.id(id;idx;name)
        6;6;need_delete
        7;7;updated
        8;8;need_update
        11;11;need_post
        12;12;need_unpost
        19;19;enable
        20;20;disable

    lock_id: statuses.id(id;idx;name)
        19;19;enable
        20;20;disable

    """
    __tablename__ = 'accounts'
    balans = relationship("AccountBalance", backref="account", foreign_keys="AccountBalance.account_id")

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('accounts.id'), nullable=True)
    number = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type_id = Column(Integer, ForeignKey('account_types.id'))
    status_id = Column(Integer, ForeignKey('statuses.id'))
    lock_id = Column(Integer, ForeignKey('statuses.id'))
    subcounto_id = Column(Integer, ForeignKey('subcountos.id'))

    edited_date = Column(DateTime, default=datetime.utcnow)

    history_list_id = Column(Integer, ForeignKey('history_accounts.id'), nullable=True, default=None)

    # Зв'язок з історією
    history_records = relationship(
        "HistoryAccount",
        backref="original_account",
        primaryjoin="HistoryAccount.parent_id == Account.id"
    )
    def __repr__(self):
        parent_name = f"'{self.parent.name}'" if self.parent_id and self.parent else "None"
        return f"<Account(number={self.number}, name={self.name}, parent_name={parent_name})>"


    # @validates('parent_id')
    # def validate_parent_account(self, key, parent_account_id):
    #     if parent_account_id == self.id:
    #         raise ValueError("Account cannot reference its own ID.")
    #     parent = parent_account_id
    #     while parent:
    #         if parent == self.id:
    #             raise ValueError("Cyclic reference detected in parent_account.")
    #         parent = session.query(Account).get(parent).parent_id
    #     return parent_account_id
    #
    #
    # @add_version_record  # Decorator for saving versions
    # def save(self, session):
    #     """Saves changes or new account to database."""
    #     session.add(self)
    #     session.commit()
    #     session.expire_all()
    #
    # # def add(session, number, name, type_id, status_id, lock_id, parent_id=None):
    # def add(session, **kwargs):
    #     """Adds a new account to the database."""
    #     new_row = AccountBalance(**kwargs)
    #     session.add(new_row)
    #     # new_account = Account(
    #     #     number=number,
    #     #     name=name,
    #     #     type_id=type_id,
    #     #     status_id=status_id,
    #     #     lock_id=lock_id,
    #     #     parent_id=parent_id
    #     # )
    #
    #     try:
    #         # session.add(new_account)
    #         # session.commit()
    #         new_row.save(session)  #save з декоратором
    #         print(f"Account '{new_row.name}' added successfully.")
    #     except IntegrityError as e:
    #         session.rollback()
    #         print(f"Error: Could not add account '{new_row.name}'. {e}")
    #     except ValueError as e:
    #         session.rollback()
    #         print(f"Validation Error: {e}")


class AccountBalance(Base):
    __tablename__ = 'account_balance'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    balance = Column(Integer, default=0)
    sales_dt = Column(Integer)
    sales_kt = Column(Integer)
    decimal_point_price = Column(Integer, default=2)

    currency = relationship("Currency", backref="balances")


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    code = Column(String(3), unique=True)  # e.g., 'USD', 'EUR'
    name = Column(String)
