import json

from src.actions import add_entry
from src.models import Entry
from src.phonebook import PhoneBook
from src.schemas import EditEntry, FindEntry
from src.settings import TEST_PHONEBOOK_PATH
from tests.conftest import ADDED_ENTRIES, _add_entry


def test_add_entry(phonebook: PhoneBook):
    """
    Тестирование добавления записи
    """

    with open(file=TEST_PHONEBOOK_PATH, mode="r") as file:
        count_lines_before_add_entry = len(file.readlines())

    good_entry = {
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "middle_name": "Ivanovich",
        "organization": "Ivanovka",
        "office_phone": "+71234567890",
        "personal_phone": "81234567890"
    }

    entry_with_bad_office_phone_number = good_entry.copy()
    entry_with_bad_office_phone_number["office_phone"] = "+7123456789a"

    entry_with_bad_personal_phone_number = good_entry.copy()
    entry_with_bad_personal_phone_number["personal_phone"] = "1234567890"

    entry_with_bad_first_name = good_entry.copy()
    entry_with_bad_first_name["first_name"] = "99"

    entry_without_last_name = good_entry.copy()
    entry_without_last_name["last_name"] = ""

    entry_with_only_first_name_and_last_name = {
        "first_name": "Ivan",
        "last_name": "Ivanov",
    }

    # good
    assert add_entry(phonebook, data=good_entry) is None
    assert (
        add_entry(phonebook, data=entry_with_only_first_name_and_last_name)
        is None
    )

    with open(file=TEST_PHONEBOOK_PATH, mode="r") as file:
        count_lines_after_add_entry = len(file.readlines())

    assert (
        count_lines_before_add_entry + ADDED_ENTRIES ==
        count_lines_after_add_entry
    )

    # bad
    assert add_entry(phonebook, data=entry_with_bad_office_phone_number
                     ).errors()[0].get("loc")[0] == "office_phone"
    assert add_entry(phonebook, data=entry_with_bad_personal_phone_number
                     ).errors()[0].get("loc")[0] == "personal_phone"
    assert add_entry(phonebook, data=entry_with_bad_first_name
                     ).errors()[0].get("loc")[0] == "first_name"
    assert add_entry(phonebook, data=entry_without_last_name
                     ).errors()[0].get("loc")[0] == "last_name"


def test_find_entry(phonebook: PhoneBook):
    """
    Тестирование поиска записи
    """

    # добавим две записи
    data_one = {
        "id": 1,
        "first_name": "Alex",
        "last_name": "asd",
        "middle_name": "asd",
        "organization": "AAA",
        "office_phone": "+71234567890",
        "personal_phone": "+71234567890"
    }

    data_two = {
        "id": 2,
        "first_name": "Lex",
        "last_name": "asd",
        "middle_name": "asd",
        "organization": "OOO",
        "office_phone": "81234567890",
        "personal_phone": "81234567890"
    }

    entry_one = _add_entry(data_one)
    entry_two = _add_entry(data_two)

    query_with_only_id = {"id": entry_one.id}
    query_with_only_first_and_last_name = {
        "first_name": entry_two.first_name,
        "last_name": entry_two.last_name
    }
    query_with_only_personal_phone = {
        "personal_phone": entry_two.personal_phone
    }

    query_with_only_id = FindEntry(**query_with_only_id)
    query_with_only_first_and_last_name = FindEntry(
        **query_with_only_first_and_last_name
    )
    query_with_only_personal_phone = FindEntry(
        **query_with_only_personal_phone
    )

    assert len(phonebook.find_entries(query_with_only_id)) == 1
    assert phonebook.find_entries(query_with_only_id)[0] == entry_one

    assert (
        len(phonebook.find_entries(query_with_only_first_and_last_name)) == 1
    )
    assert (
        phonebook.find_entries(query_with_only_first_and_last_name)[0] ==
        entry_two
    )

    assert len(phonebook.find_entries(query_with_only_personal_phone)) == 1
    assert (
        phonebook.find_entries(query_with_only_personal_phone)[0] == entry_two
    )

    assert len(phonebook.find_entries(FindEntry())) == ADDED_ENTRIES


def test_edit_entry(phonebook: PhoneBook):
    """
    Тестирование изменения записи
    """

    # добавим две записи
    data_one = {
        "id": 1,
        "first_name": "Alex",
        "last_name": "asd",
        "middle_name": "asd",
        "organization": "AAA",
        "office_phone": "+71234567890",
        "personal_phone": "+71234567890"
    }

    data_two = {
        "id": 2,
        "first_name": "Lex",
        "last_name": "asd",
        "middle_name": "asd",
        "organization": "OOO",
        "office_phone": "81234567890",
        "personal_phone": "81234567890"
    }

    entry_one = _add_entry(data_one)
    entry_two = _add_entry(data_two)

    new_data = {
        "first_name": "Edit",
        "last_name": "Edit",
        "middle_name": "",
        "organization": "",
        "office_phone": "",
    }

    new_entry = EditEntry(**new_data)

    phonebook.edit_entry(id=entry_one.id-1, data=new_entry)

    with open(TEST_PHONEBOOK_PATH, "r") as file:
        first_entry = Entry(**json.loads(next(file)))
        second_entry = Entry(**json.loads(next(file)))

    assert first_entry.first_name == new_data["first_name"]
    assert first_entry.last_name == new_data["last_name"]
    assert first_entry.office_phone == entry_one.office_phone
    assert first_entry.personal_phone == entry_one.personal_phone

    assert second_entry == entry_two
