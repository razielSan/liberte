from typing import Protocol


class ModuleSettingsContract(Protocol):
    # Идентификатор модуля (уникальный)
    SERVICE_NAME: str

    # Где лежит код
    ROOT_PACKAGE: str

    # FS
    NAME_FOR_TEMP_FOLDER: str
    NAME_FOR_LOG_FOLDER: str


REQUIRED_FIELDS_MODULES = {
    "SERVICE_NAME",
    "ROOT_PACKAGE",
    "NAME_FOR_TEMP_FOLDER",
    "NAME_FOR_LOG_FOLDER",
}


