def load_some_data_to_database():
    config = conf_db.DatabasesConfig()
    session = config.create_session()

    try:
        # Добавление тестовых данных для User
        user1 = model.User(name="John Doe", password="password123", level_id=1, status=0)
        user2 = model.User(name="Jane Smith", password="password456", level_id=2, status=1)
        session.add(user1, user2)

        # Добавление тестовых данных для AccessLevel
        access_level1 = AccessLevel(name="Admin", level=1)
        access_level2 = AccessLevel(name="User", level=2)
        session.add(access_level1, access_level2)

        # Добавление тестовых данных для Comment
        comment1 = Comment(comments="Initial comment", old_comments=None)
        comment2 = Comment(comments="Updated comment", old_comments="Initial comment")
        session.add(comment1, comment2)

        # Добавление тестовых данных для AssociatedAccount
        associated_account1 = AssociatedAccount(root_dt=1, root_kt=2, name="Primary Account")
        associated_account2 = AssociatedAccount(root_dt=3, root_kt=4, name="Secondary Account")
        session.add(associated_account1, associated_account2)

        # Добавление тестовых данных для DocumentType
        document_type1 = DocumentType(type=1, name="Invoice")
        document_type2 = DocumentType(type=2, name="Receipt")
        session.add(document_type1, document_type2)

        # Добавление тестовых данных для Status
        status1 = Status(idx=1, name="Approved")
        status2 = Status(idx=2, name="Pending")
        session.add(status1, status2)

        # Добавление тестовых данных для QrCode
        qr_code1 = QrCode(number=12345)
        qr_code2 = QrCode(number=67890)
        session.add(qr_code1, qr_code2)

        # Добавление тестовых данных для Document
        document1 = Document(number=1001, type_id=1, lock=0)
        document2 = Document(number=1002, type_id=2, lock=1)
        session.add(document1, document2)

        # Добавление тестовых данных для Operation
        operation1 = Operation(document_id=1, number=1)
        operation2 = Operation(document_id=2, number=2)
        session.add(operation1, operation2)

        # Добавление тестовых данных для Transaction
        transaction1 = Transaction(operation_id=1, price=1000, quantity=10, summ=10000, status_id=1, type=1)
        transaction2 = Transaction(operation_id=2, price=500, quantity=5, summ=2500, status_id=2, type=2)
        session.add(transaction1, transaction2)

        # Добавление тестовых данных для AccountType
        account_type1 = AccountType(name="System Account")
        account_type2 = AccountType(name="User Account")
        session.add(account_type1, account_type2)

        # Добавление тестовых данных для Unit
        unit1 = Unit(number=1, name="Root Unit", full_name="Root Unit Full Name", point_type=0)
        unit2 = Unit(number=2, name="Sub Unit", full_name="Sub Unit Full Name", point_type=1, parent_id=1)
        session.add(unit1, unit2)

        # Добавление тестовых данных для SubcountoBalance
        subcounto_balance1 = SubcountoBalance(subcounto_id=1, currency_id=1, balance=1000)
        subcounto_balance2 = SubcountoBalance(subcounto_id=2, currency_id=2, balance=2000)
        session.add(subcounto_balance1, subcounto_balance2)

        # Добавление тестовых данных для ScTransactionType
        sc_transaction_type1 = ScTransactionType(name="Service", description="Service Transaction")
        sc_transaction_type2 = ScTransactionType(name="Product", description="Product Transaction")
        session.add(sc_transaction_type1, sc_transaction_type2)

        # Добавление тестовых данных для ScTransaction
        sc_transaction1 = ScTransaction(subcounto_id=1, number=1, quantity=10, price=100)
        sc_transaction2 = ScTransaction(subcounto_id=2, number=2, quantity=5, price=50)
        session.add(sc_transaction1, sc_transaction2)

        # Добавление тестовых данных для SubcountoType
        subcounto_type1 = SubcountoType(number=1, name="Root", full_name="Root Type Full Name")
        subcounto_type2 = SubcountoType(number=2, name="Dir", full_name="Dir Type Full Name")
        session.add(subcounto_type1, subcounto_type2)

        # Добавление тестовых данных для Subcounto
        subcounto1 = Subcounto(number=1, name="Root Subcounto", full_name="Root Subcounto Full Name")
        subcounto2 = Subcounto(number=2, name="Child Subcounto", full_name="Child Subcounto Full Name", parent_id=1)
        session.add(subcounto1, subcounto2)

        # Добавление тестовых данных для HistoryAccount
        history_account1 = HistoryAccount(number=1, name="History Account 1")
        history_account2 = HistoryAccount(number=2, name="History Account 2")
        session.add(history_account1, history_account2)

        # Добавление тестовых данных для Account
        account1 = Account(number=1, name="Main Account", type_id=1)
        account2 = Account(session=session, number=2, name="Secondary Account", type_id=2, parent_id=1)
        session.add(account1, account2)

        # Добавление тестовых данных для AccountBalance
        account_balance1 = AccountBalance(account_id=1, currency_id=1, balance=5000)
        account_balance2 = AccountBalance(account_id=2, currency_id=2, balance=3000)
        session.add(account_balance1, account_balance2)

        # Добавление тестовых данных для Currency
        currency1 = Currency(code="USD", name="US Dollar")
        currency2 = Currency(code="EUR", name="Euro")
        session.add(currency1, currency2)

        # Коммит всех изменений
        session.commit()
        print("Test data loaded successfully.")

    except Exception as e:
        session.rollback()
        print(f"Error: Could not load test data. {e}")
    finally:
        session.close()



def load_data_from_csv(session, model, csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            session.add(model(**row))


# Database Configuration Setup
config = conf_db.DatabasesConfig()
session = config.create_session()

try:
    # Load data from CSV files for each model
    load_data_from_csv(session, User, 'User.csv')
    load_data_from_csv(session, AccessLevel, 'AccessLevel.csv')
    load_data_from_csv(session, Comment, 'Comment.csv')
    load_data_from_csv(session, AssociatedAccount, 'AssociatedAccount.csv')
    load_data_from_csv(session, DocumentType, 'DocumentType.csv')
    load_data_from_csv(session, Status, 'Status.csv')
    load_data_from_csv(session, QrCode, 'QrCode.csv')
    load_data_from_csv(session, Document, 'Document.csv')
    load_data_from_csv(session, Operation, 'Operation.csv')
    load_data_from_csv(session, Transaction, 'Transaction.csv')
    load_data_from_csv(session, AccountType, 'AccountType.csv')
    load_data_from_csv(session, Unit, 'Unit.csv')
    load_data_from_csv(session, SubcountoBalance, 'SubcountoBalance.csv')
    load_data_from_csv(session, ScTransactionType, 'ScTransactionType.csv')
    load_data_from_csv(session, ScTransaction, 'ScTransaction.csv')
    load_data_from_csv(session, SubcountoType, 'SubcountoType.csv')
    load_data_from_csv(session, Subcounto, 'Subcounto.csv')
    load_data_from_csv(session, HistoryAccount, 'HistoryAccount.csv')
    load_data_from_csv(session, Account, 'Account.csv')
    load_data_from_csv(session, AccountBalance, 'AccountBalance.csv')
    load_data_from_csv(session, Currency, 'Currency.csv')

    # Коммит всех изменений
    session.commit()
    print("Test data loaded successfully from CSV files.")

except Exception as e:
    session.rollback()
    print(f"Error: Could not load test data. {e}")
finally:
    session.close()