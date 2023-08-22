import os

import pytest

from src.models import Entry
from src.phonebook import PhoneBook
from src.settings import TEST_PHONEBOOK_PATH


ADDED_ENTRIES = 2


@pytest.fixture(autouse=True, scope="function")
def tmp_file():
    with open(TEST_PHONEBOOK_PATH, "w"):
        yield
    os.remove(TEST_PHONEBOOK_PATH)


@pytest.fixture(scope="session")
def phonebook():
    return PhoneBook(TEST_PHONEBOOK_PATH)


def _add_entry(data: dict) -> Entry:
    """
    Добавление записи
    """

    entry = Entry(**data)

    with open(file=TEST_PHONEBOOK_PATH, mode="a+") as file:
        file.write(entry.model_dump_json() + "\n")

    return entry
