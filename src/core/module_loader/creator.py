from pathlib import Path

from typing import Dict, List
from pathlib import Path

from core.response.response_data import ResponseData
from core.constants import DEFAULT_CHILD_SEPARATOR
from core.module_loader.templates import TEMPLATE_DIRS, TEMPLATE_FILES


def generate_content(template: str, **kwargs):
    """
    Подставляет значения в строке на переданные.
    """

    for key, value in kwargs.items():
        template = template.replace(f"{{{key}}}", value)
    return template


def create_module(
    root_dir: Path,
    root_package: str,
    module_name: str,
    separator: str = DEFAULT_CHILD_SEPARATOR,
    template_dirs: Dict = TEMPLATE_DIRS,
    template_files: Dict = TEMPLATE_FILES,
) -> ResponseData:
    """
    Создает модуль и все вложенные модули

    Дочерние модули будут разделены

    Архитектура модуля:

    api/
    fsm/
    services/
    utils/
    keyboards/
    childes/
    __init__.py
    extensions.py
    router.py
    settings.py
    response.py
    logging.py

    Args:
        root_dir (Path): Путь до корневой директории проекта
        root_package: (str): Путь для импорта, начинается с корневой директории

        Пример
        app.bot.modules

        module_name: Имя модуля.Дочение модули разделяются "."

        Пример
        test.test

        separator: (str): Имя для связывыния дочернего и родительского модуля

        Имя папки для хранения дочерних модулей, формирования имен в settings,
        формирования имени роутера

        template_dirs: (Dict): Шаблон с директориями для создания модуля
        template_files: (Dict): Шаблон с файлами для создания модуля


    Returns:
        RepsonseData: объект содержащий в себе

        Атрибуты ResponseData:
            - message (Any | None): Содержание ответа. None если произошла ошибка
            - error (str | None): Текст ошибки если есть если нет то None
    """

    list_modules: List[str] = module_name.split(".")  # разделяем имя модуля для
    # создания родетельских и дочерних модулей
    parent_name: str = list_modules[0]  # родительское имя модуля
    full_name = None
    package = None
    module_path = None
    for index, name in enumerate(list_modules, start=1):
        if index == 1:  # если родительский модуль
            full_name = name
            package = f"{root_package}.{name}"
            module_path = root_dir / Path(package.replace(".", "/"))
        else:
            full_name = f"{full_name}.{separator}.{name}"
            package = f"{package}.{separator}.{name}"
            module_path = root_dir / Path(package.replace(".", "/"))

        if module_path.exists():
            continue

        module_path.mkdir(parents=True, exist_ok=True)
        for filename, content in template_files.items():
            filepath: Path = module_path / filename
            temp_path: str = full_name.replace(".", "/")
            log_name: str = full_name.split(".")[0]
            if not filepath.exists():
                content: str = generate_content(
                    log_name=log_name,
                    template=content,
                    name=full_name,
                    temp_path=temp_path,
                    root_package=package,
                    path_to_module=f"{temp_path}/{separator}",
                    root_childes=f"{package}.{separator}",
                    root_router_name=parent_name,
                )
            filepath.write_text(data=content, encoding="utf-8")
        for dir_name in template_dirs:
            directory: Path = module_path / dir_name
            directory.mkdir(exist_ok=True)
            init_file: Path = directory / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# init\n")
    print("Modul create succeffuly")
    return ResponseData(message="success", error=None)


def creates_new_modules_via_the_command_line(
    root_dir: Path,
    module_name: str,
    root_package: str,
    template_dirs: Dict = TEMPLATE_DIRS,
    template_files: Dict = TEMPLATE_FILES,
    separator: str = DEFAULT_CHILD_SEPARATOR,
) -> None:
    """
    Создает новые модули для бота через командную строку.

    Дочерний модуль должен быть разделен '.' от родительского модуля.
    Пример:

    cli add-module video.test.data

    """
    data: ResponseData = create_module(
        module_name=module_name,
        root_package=root_package,
        root_dir=root_dir,
        template_files=template_files,
        template_dirs=template_dirs,
        separator=separator,
    )
    if data.error:
        print(data.error)
    else:
        print(f"Modules {module_name} created successfully")
