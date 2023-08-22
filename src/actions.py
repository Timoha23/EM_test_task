import json
from json import JSONDecodeError

from pydantic import ValidationError

from src.models import Entry
from src.phonebook import PhoneBook
from src.schemas import CreateEntry, EditEntry, FindEntry


def add_entry(pb: PhoneBook, data: dict = None) -> None:
    """
    Обработчик консольной команды "add_entry"

    :Args:
        - pb - объект класса PhoneBook
        - data - данные о записи. Данный параметр предназначен для
                 тестов
    """

    if data is None:
        cmds = {
            "first_name": "Введите имя: ",
            "last_name": "Введите фамилию: ",
            "middle_name": "Введите отчество: ",
            "organization": "Введите организацию: ",
            "office_phone": "Введите рабочий телефон: ",
            "personal_phone": "Введите личный телефон: ",
        }
        data = {}

        for key, cmd in cmds.items():
            value = input(cmd)
            if value == "":
                value = None
            data[key] = value

    try:
        entry = CreateEntry.model_validate(data)
        pb.add_entry(entry=entry)
        print("Запись успешно добавлена.")
    except ValidationError as ex:
        print(ex)
        return ex


def show_entries(pb: PhoneBook) -> None:
    """
    Обработчик консольной команды "show_entries"

    :Args:
        - pb - объект класса PhoneBook
    """

    items_gen = pb.get_entries()

    first_page = True

    for items in items_gen:
        if not first_page:
            input("Нажмите клавишу Enter для вывода следующих записей...")
        for item in items:
            entry = json.loads(item)
            print(Entry(**entry))
        first_page = False
    print("Записей нет.")


def find_entry(pb: PhoneBook) -> None | Exception:
    """
    Обработчик консольной команды "find_entry"

    :Args:
        - pb - объект класса PhoneBook
        - data - данные для поиска записи. Данный параметр предназначен
                 для тестов
    """

    data = input(
        'Введите данные в формате json\nПример ввода данных: {"id": 1, '
        '"first_name": "Ivan", "office_phone": "+71234567890", '
        '"personal_phone": null}\n'
        'Примечание: можно искать по любому параметру: '
    )
    try:
        data = json.loads(data)
        data = FindEntry.model_validate(data)
        entries = pb.find_entries(data=data)
        if len(entries) == 0:
            print("По вашему запросу записей не найдено.")
        else:
            print(f"По вашему запросу найдено {len(entries)} записей.")
        for entry in entries:
            print(entry)
    except ValidationError as ex:
        print(ex)
        return ex
    except JSONDecodeError as ex:
        print(ex)
        return ex


def edit_entry(pb: PhoneBook) -> None | Exception:
    """
    Обработчик консольной команды "edit_entry"

    :Args:
        - pb - объект класса PhoneBook
    """

    try:
        entry_id = int(input("Введите ID записи для редактирования: "))
    except ValueError:
        print("Необходимо ввести число.")
        return
    if entry_id < 1:
        print("ID не может быть меньше либо равен нулю.")
        return
    try:
        data = input("Введите данные в формате json: ")
        data = json.loads(data)
        data = EditEntry.model_validate(data)
        pb.edit_entry(int(entry_id) - 1, data=data)
        print("Запись успешно обновлена.")
    except StopIteration as ex:
        print("Запись с таким ID не существует.")
        return ex
    except ValidationError as ex:
        print(ex)
        return ex
    except JSONDecodeError as ex:
        print(ex)
        return ex
