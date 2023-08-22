import re

from pydantic import BaseModel, Field, field_validator


NAMES_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z]+$")
PHONE_PATTERN = re.compile(r"^(8|\+7)[0-9]{5,15}+$")


class Entry(BaseModel):
    """
    Модель записи
    """

    id: int
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    middle_name: str | None = None
    organization: str | None = None
    office_phone: str | None = None
    personal_phone: str | None = None

    @field_validator("first_name", "last_name", "middle_name")
    def validate_first_last_and_middle_names(cls, value: str) -> str:
        if value is not None and not NAMES_PATTERN.match(value):
            raise ValueError(
                f"Некорректные данные: {value}. Данное поле может "
                f"включать только символы кириллицы и латиницы"
            )
        return value

    @field_validator("office_phone", "personal_phone")
    def validate_office_and_personal_phone(cls, value: str) -> str:
        if value is not None and not PHONE_PATTERN.match(value):
            raise ValueError(f"Некорректный номер телефона: {value}")
        return value

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Имя: {self.first_name}\n"
            f"Фамилия: {self.last_name}\n"
            f"Отчество: {self.middle_name}\n"
            f"Организация: {self.organization}\n"
            f"Рабочий телефон: {self.office_phone}\n"
            f"Личный телефон: {self.personal_phone}\n"
        )
