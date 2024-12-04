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

#create_user("test_user1", "password1", status="enable")
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

#get_all_users()

#Зміна пароль на логіну

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


#TODO: Функції сет статус (иф нон в айді в моделі делає нову строчку пусту а в параметрах) і гет статус,
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

create_empty_document()


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


