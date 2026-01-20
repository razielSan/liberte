from typing import Protocol


class ModuleSettingsContract(Protocol):
    # Идентификатор модуля (уникальный)
    SERVICE_NAME: str

    # Где лежит код
    ROOT_PACKAGE: str

    # Флаг проверки для главного меню
    SHOW_IN_MAIN_MENU: bool

    # FS
    NAME_FOR_TEMP_FOLDER: str
    NAME_FOR_LOG_FOLDER: str


DEFAULT_FIELD_FOR_INLINE_MENU_DATA: str = "MENU_CALLBACK_DATA"
DEFAULT_FIELD_FOR_INLINE_MENU_TEXT: str = "MENU_CALLBACK_TEXT"

REQUIRED_FIELDS_MODULES = {
    "SERVICE_NAME",
    "ROOT_PACKAGE",
    "NAME_FOR_TEMP_FOLDER",
    "NAME_FOR_LOG_FOLDER",
    "SHOW_IN_MAIN_MENU",
}
