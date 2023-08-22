import itertools
import json
import os
from typing import Generator

from src.models import Entry
from src.schemas import CreateEntry, EditEntry, FindEntry
from src.settings import ITEMS_ON_PAGE


class PhoneBook:
    def __init__(self, path: str) -> None:
        """
        :Args:
            - path - путь к файлу PhoneBook
        """
        self.path = path

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        path = kwargs.get("path")
        if not os.path.exists(path):
            with open(file=path, mode="w"):
                ...
        return instance

    def add_entry(self, entry: CreateEntry) -> Entry:
        """
        Добавление записи в телефонную книгу

        :Args:
            - entry - Объект CreateEntry
        """

        with open(file=self.path, mode="a") as file:
            entry.id = self._get_count_lines() + 1
            file.write(entry.model_dump_json() + "\n")

        return entry

    def edit_entry(self, id: int, data: EditEntry) -> None:
        """
        Редактирование записи в телефонной книги

        :Args:
            - id - ID записи
            - data - Объект EditEntry, которой содержит
                     данные о записи для изменения
        """

        entry = self._find_entry_by_id(id=id)
        new_entry = entry.model_dump()
        for key, value in data.model_dump().items():
            if value is not None and value != "":
                new_entry[key] = value

        new_entry = Entry(**new_entry)
        with open(file=self.path, mode="r") as file:
            filedata = file.read()
        new_filedata = filedata.replace(
            entry.model_dump_json(),
            new_entry.model_dump_json()
        )

        with open(file=self.path, mode="r+") as file:
            file.write(new_filedata)

    def find_entries(self, data: FindEntry) -> list[Entry]:
        """
        Поиск записей по одной или нескольким характеристикам

        :Args:
            - data - Объект FindEntry который содержит
                     характеристики для поиска
        """

        entries = []

        with open(file=self.path, mode="r") as file:
            for line in file:
                found = True
                entry = json.loads(line)
                for key, value in data.model_dump().items():
                    if value is None:
                        continue
                    if entry.get(key) == value:
                        pass
                    else:
                        found = False
                        break
                if found:
                    entries.append(Entry(**entry))

        return entries

    def _get_count_lines(self) -> int:
        """
        Получение количества строк в телефонной книге
        """

        with open(file=self.path, mode="r") as file:
            lines = len(file.readlines())

        return lines

    def get_entries(self) -> Generator[list[str], None, None]:
        """
        Генератор для получения строк из телефонной книги
        """

        skip = 0
        count_lines = self._get_count_lines()

        with open(file=self.path, mode="r") as file:
            while skip <= count_lines:
                if skip + ITEMS_ON_PAGE > count_lines:
                    end = count_lines
                else:
                    end = skip + ITEMS_ON_PAGE
                lines = [next(file) for _ in range(skip, end)]
                yield lines
                skip += ITEMS_ON_PAGE

    def _find_entry_by_id(self, id: int) -> Entry:
        """
        Поиск записи по ID

        :Args:
            - id - ID записи
        """

        with open(file=self.path, mode="r") as file:
            entry = json.loads(next(itertools.islice(file, id, None)))
            return Entry(**entry)
