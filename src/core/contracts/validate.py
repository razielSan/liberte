from pathlib import Path
from typing import List
from types import ModuleType

from core.contracts.constants import (
    DEFAULT_NAME_SETTINGS,
    DEFAULT_NAME_ROUTER,
    REQUIERED_MODULE_DIRS,
)
from core.contracts.module import REQUIRED_FIELDS_MODULES
from core.response.response_data import Result
from core.error_handlers.helpers import ok, fail
from core.error_handlers.helpers import safe_import


def validate_module_structure(
    path: Path,
    name_settings: str = DEFAULT_NAME_SETTINGS,
    name_router: str = DEFAULT_NAME_ROUTER,
    requiered_directory: List = REQUIERED_MODULE_DIRS,
) -> Result:
    required = [f"{name_settings}.py", f"{name_router}.py"]

    for file in required:
        if not (path / file).exists():
            return fail(
                code="Invalide module",
                message=f"Invalide module structure : {file} missing",
            )
    for directory in requiered_directory:
        if not (path / directory).exists():
            return fail(
                code="Invalide module",
                message=f"Invalide module structure : {directory} directory missing",
            )

    return ok(data="success")


def validate_module_settings(
    root_package: str,
    required_field_modules: set = REQUIRED_FIELDS_MODULES,
    name_settings: str = DEFAULT_NAME_SETTINGS,
) -> Result:

    result_import: Result = safe_import(
        module_path=f"{root_package}.{name_settings}",
    )
    if not result_import.ok:
        return result_import

    module_settings: ModuleType = result_import.data

    settings = getattr(module_settings, f"{name_settings}")

    modules_set = set(
        settings.model_fields.keys()
    )  # получаем множество из имен полей модели
    result_settings = required_field_modules.difference(modules_set)
    if (
        result_settings
    ):  # если осталось хоть одно поле значит его нет в загруженной модели
        return fail(
            code="Invalide module",
            message=f"Invalide module settings : {result_settings} missing",
        )

    return ok(data="success")
