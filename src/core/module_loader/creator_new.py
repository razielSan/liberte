from pathlib import Path


from typing import List
from pathlib import Path

from core.response.response_data import ResponseData
from core.module_loader.templates import TEMPLATATE_DIRS, TEMPLATE_FILES


def generate_content(template: str, **kwargs):
    for key, value in kwargs.items():
        template = template.replace(f"{{{key}}}", value)
    return template


def create_module(
    root_dir: Path,
    module_name: str,
    root_package: str,
) -> ResponseData:
    """
    Создает модуль и все вложенные модули

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
        list_path_modules (List[str]): Список из названий путей модулей.
        Если модуль дочерний, то название должно быть разделено childes/

        Пример:
        ["video/childes/main", "audio]

        Создаст:
            video/
                childes/__init__.py
                __init__.py
                settings.py
                router.py
                ...
            video/childes/main/
                childes/__init__.py
                __init__.py
                settings.py
                router.py
                ...
            audio/
                childes/__init__.py
                __init__.py
                settings.py
                router.py
                ...


        path_to_modules (Path): путь до папки с модулями
        root_package (str): Путь для импорта, начинается с корневой директории

        Пример:
        app.bot.modules

    Returns:
        RepsonseData: объект содержащий в себе

        Атрибуты ResponseData:
            - message (Any | None): Содержание ответа. None если произошла ошибка
            - error (str | None): Текст ошибки если есть если нет то None
    """

    list_modules = module_name.split(".")
    parent_name = list_modules[0]
    full_name = None
    package = None
    module_path = None
    for index, name in enumerate(list_modules, start=1):
        if index == 1:  # если родительский модуль
            full_name = name
            package = f"{root_package}.{name}"
            module_path = root_dir / Path(package.replace(".", "/"))
        else:
            full_name = f"{full_name}.childes.{name}"
            package = f"{package}.childes.{name}"
            module_path = root_dir / Path(package.replace(".", "/"))
        module_path.mkdir(parents=True, exist_ok=True)
        for filename, content in TEMPLATE_FILES.items():
            filepath = module_path / filename
            temp_path = full_name.replace(".", "/")
            if not filepath.exists():
                content = generate_content(
                    template=content,
                    name=full_name,
                    temp_path=temp_path,
                    root_package=package,
                    path_to_module=f"{temp_path}/childes",
                    root_childes=f"{package}.childes",
                    root_router_name=parent_name,
                )
            print(module_path)
            filepath.write_text(data=content, encoding="utf-8")
        for dir_name in TEMPLATATE_DIRS:
            directory: Path = module_path / dir_name
            directory.mkdir(exist_ok=True)
            init_file: Path = directory / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# init\n")
    print("Modul create succeffuly")
    return ResponseData(message="success")


def creates_new_modules_via_the_command_line(
    root_dir: Path,
    module_name: str,
    root_package: str,
) -> None:
    """
    Создает новые модули для бота через командную строку.

    Дочерний модуль должен быть разделен 'childes' от родительского модуля.
    Пример:

    cli add-module video video/childes/create audio

    args:
        list_path_modules(List[str]): Список из имен путей модулей

        Пример
        ['video/childes/main', "audio"]

        module_path (Path):  Путь до папки с модулями
        root_package (str): Путь для импорта, начинается с корневой директории

        Пример:
        app.bot.modules

    """
    data: ResponseData = create_module(
        module_name=module_name,
        root_package=root_package,
        root_dir=root_dir
    )
    if data.error:
        print(data.error)
    else:
        print(f"Modules {module_name} created successfully")
