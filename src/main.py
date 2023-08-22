import sys

from src.actions import add_entry, edit_entry, find_entry, show_entries
from src.phonebook import PhoneBook
from src.settings import PHONEBOOK_PATH


def main() -> None:
    pb = PhoneBook(path=PHONEBOOK_PATH)

    commands = {
        "add_entry": {
            "function": add_entry,
            "description": "Добавить запись",
        },
        "show_entries": {
            "function": show_entries,
            "description": "Показать записи",
        },
        "find_entry": {
            "function": find_entry,
            "description": "Найти запись",
        },
        "edit_entry": {
            "function": edit_entry,
            "description": "Изменить запись",
        },
    }

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        command = commands.get(arg)
        if command is None:
            helper = ""
            for key in commands:
                helper += f"{key} - {commands[key]['description']}\n"
            print(f"Команда не найдена. Список доступных команд:\n"
                  f"{helper}")
            return
        command["function"](pb)


if __name__ == "__main__":
    main()
