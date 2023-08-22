from pydantic import BaseModel

from src.models import Entry


class CreateEntry(Entry):
    """
    Создание записи
    """

    id: int | None = None


class EditEntry(BaseModel):
    """
    Редактирование записи
    """

    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    organization: str | None = None
    office_phone: str | None = None
    personal_phone: str | None = None


class FindEntry(EditEntry):
    """
    Поиск записи
    """

    id: int | None = None
