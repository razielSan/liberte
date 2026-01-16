import importlib
from collections import defaultdict
import pkgutil
from typing import List
from types import ModuleType

from core.response.modules_loader import ModuleInfo
from core.constants import DEFAULT_CHILD_SEPARATOR


def get_root_and_parent(
    module_name: str,
    root_package: str,
    separator: str = DEFAULT_CHILD_SEPARATOR,
) -> List[str]:
    """
    Проверка имени модуля на родительский и дочерний.

    Args:
        module_name: Имя модуля
        root_package: (str): Путь для импорта
        separator: (str): Имя для связывыная дочернего и родительского модуля

    Returns:
        List[str]:

        Возвращает кортеж из двух параметров

        ("<root_module_name>", "<root_module_name>") - если модуль дочерний
        ("<root_module_name>", None) - если модуль) - если модуль корневой
    """

    relative = module_name.replace(root_package + ".", "")  # отсекаем
    # путь до модуля оставляя только имя - app.bot.modules.test -> test
    parts = relative.split(f".{separator}.")

    root = parts[0].split(".")[
        0
    ]  # отсекаем название файла если роутер корневой - test.router -> test
    parent = root if len(parts) > 1 else None
    return root, parent


def load_modules(
    root_package: str,
    separator: str = DEFAULT_CHILD_SEPARATOR,
) -> List[ModuleInfo]:
    """
    Проходится по модулям и возвращает обьект ModuleInfo c собранными
    данными

    Args:
        root_package: (str): Путь для импорта, начинается с корневой директории

        Пример
        app.bot.modules

        separator: (str): Имя для связывания дочернего и родительского модуля
        
        Имя папки для хранения дочерних модулей, формирования имен в settings, 
        формирования имени роутера

    Returns:       
        List[ModuleInfo]: обьект содержащий в себе

        Атрибуты ModuleInfo]:
            - package (str): Путь для импорта модуля
            - root (str): Имя корневого роутера
            - settings (ModuleType): Модуль с настройками
            - router (ModuleType): Модуль router
            - parent (str | None): Имя корневого роутера если дочерний если корневой то
            None
        
    """
    
    package: ModuleType = importlib.import_module(root_package)
    modules = defaultdict(dict)

    for module_info in pkgutil.walk_packages(
        path=package.__path__, prefix=package.__name__ + "."
    ):
        module_name: str = module_info.name
        if not module_name.endswith("settings") and not module_name.endswith("router"):
            continue
        root, parent = get_root_and_parent(
            module_name=module_name,
            root_package=root_package,
            separator=separator,
        )

        package_name, file_type = module_name.rsplit(".", 1)
        mod: ModuleType = importlib.import_module(module_name)
        modules[package_name][file_type] = mod
        modules[package_name]["root"] = root
        modules[package_name]["parent"] = parent
        modules[package_name]["package"] = package_name
    array_modules = []
    for package, data in modules.items():
        if "router" not in data or "settings" not in data:
            continue  # дополнительная проверка

        array_modules.append(
            ModuleInfo(
                package=data.get("package"),
                root=data.get("root"),
                parent=data.get("parent"),
                router=data.get("router"),
                settings=data.get("settings"),
            )
        )
    return array_modules
