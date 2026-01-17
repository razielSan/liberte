from pathlib import Path
import importlib
from typing import Protocol, List
from dataclasses import dataclass
import pkgutil
from types import ModuleType


from core.constants import DEFAULT_CHILD_SEPARATOR, DEFAULT_BOT_MODULES_ROOT
from core.logging.factory import LoggerFactory
from core.logging.storage import storage
from core.logging.runtime import LoggerRuntime
from core.logging.format import log_format


class BotPathProtocol(Protocol):
    BOT_DIR: Path
    TEMP_DIR: Path
    LOG_DIR: Path
    STATIC_DIR: Path


class AppPathProtocol(Protocol):
    APP_DIR: Path
    TEMP_DIR: Path
    LOG_DIR: Path
    STATIC_DIR: Path


class AppSettingsProtocol(Protocol):
    SERVICE_NAME: str


class BotSettingsProtocol(Protocol):
    SERVICE_NAME: str
    TOKEN: str
    LIST_BOT_COMMANDS: List


class ModuleSettings(Protocol):
    SERVICE_NAME: str
    MENU_REPLY_TEXT: str
    MENU_CALLBACK_TEXT: str
    MENU_CALLBACK_DATA: str
    NAME_FOR_LOG_FOLDER: str
    NAME_FOR_TEMP_FOLDER: str
    ROOT_PACKAGE: str


@dataclass
class AppContext:
    app_path: AppPathProtocol
    bot_path: BotPathProtocol
    app_settings: AppSettingsProtocol
    bot_settings: BotSettingsProtocol
    loggers: LoggerRuntime
    root_modules_settings: List[ModuleSettings]


def load_bot_paths(bot_core: str, name_variable: str = "bot_path") -> BotPathProtocol:
    """
    Возвращает обьект хранящий путь для бота.

    Args:
        bot_core (str): Путь до модуля, в котором хранятся пути для бота

        Пример:
        app.bot.core.paths

        name_variable (str): Имя переменной хранения путей бота

    Raises:
        RuntimeError: Ошибка если переменная не найдена

    Returns:
        BotPath: содержит в себе

        атрибуты BotPath:
            - BOT_DIR  (Path)
            - TEMP_DIR (Path)
            - LOG_DIR  (Path)
            - STATIC_DIR (Path)
    """
    module: ModuleType = importlib.import_module(bot_core)
    if not hasattr(module, name_variable):
        raise RuntimeError(f"{name_variable} not found")
    return module.bot_path


def load_app_paths(app_core: str, name_variable: str = "app_path") -> AppPathProtocol:
    """
    Возвращает обьект хранящий путь для приложения.

    Args:
        app_core (str): Путь до модуля, в котором хранятся пути для приложения

        Пример:
        app.core.paths

        name_variable (str): Имя переменной хранения путей приложения.

    Raises:
        RuntimeError: Ошибка если переменная не найдена

    Returns:
       AppPath: содержит в себе

        атрибуты AppPath:
            - APP_DIR  (Path)
            - TEMP_DIR (Path)
            - LOG_DIR  (Path)
            - STATIC_DIR (Path)
    """
    module: ModuleType = importlib.import_module(app_core)
    if not hasattr(module, name_variable):
        raise RuntimeError(f"{name_variable} not found")
    return module.app_path


def load_settings(core: str) -> object:
    """
    Возвращает обьект хранящий настройки.

    Args:
        core (str): Путь до модуля в котором хранятся настройки

        Пример:
        app.bot.core.settings


    Raises:
        RuntimeError: Ошибка если переменная не найдена

    Returns:
        object: содержит в себ

        атрибуты object:
            - SERVICE_NAME (str)
            ............

    """

    module = importlib.import_module(core)
    if not hasattr(module, "settings"):
        raise RuntimeError("settings not found")
    return module.settings


def load_bot_root_modules_settings(
    root_package: str,
    separator: str = DEFAULT_CHILD_SEPARATOR,
) -> List[ModuleSettings]:
    """
    Возвращает список из обьектов содержащих настройки для корневых модулей.

    Args:
        root_package (str): Путь для модуля, в котором хранятся модули

        Пример:
        app.bot.modules

        separator: (str): Имя для связывыния дочернего и родительского модуля.
        По умолчанию DEFAULT_CHILD_SEPARATOR

        Имя папки для хранения дочерних модулей, формирования имен в settings,
        формирования имени роутерадулей

    Returns:
        List[ModuleSettings]: содержит в себе

        атрибуты ModuleSettings:
            - SERVICE_NAME (str)
            - MENU_REPLY_TEXT (str)
            - MENU_CALLBACK_TEXT (str)
            - MENU_CALLBACK_DATA (str)
            - NAME_FOR_LOG_FOLDER (str)
            - NAME_FOR_TEMP_FOLDER: (str)
            - ROOT_PACKAGE: (str)

    """
    package: ModuleType = importlib.import_module(root_package)  # получаем модуль
    array_settings: List = []  # список для настроек
    for module_info in pkgutil.walk_packages(
        path=package.__path__, prefix=package.__name__ + "."
    ):  # проходимся по пакетам модуля
        name: str = module_info.name

        if not name.endswith("settings"):  # если не настройки
            continue

        if separator in name:  # если дочерний то пропускаем итерацию
            continue

        module_settings: ModuleType = importlib.import_module(name=name)

        if not hasattr(module_settings, "settings"):
            raise RuntimeError("settings not found")

        setttings = getattr(module_settings, "settings")

        array_settings.append(setttings)
    return array_settings


def init_logging(
    app_path: AppPathProtocol,
    bot_path: BotPathProtocol,
    app_settings: object,
    bot_settings: object,
    root_modules_settings: List[ModuleSettings],
) -> LoggerRuntime:
    """
    Ининициализирует логи.

    Возвращат обьект содержий в себе проинициализированные логи

    Args:
        app_path (AppPathProtocol): Обьект содержащий пути для приложения
        bot_path (BotPathProtocol): Обьект содержащий пути для бота
        app_settings (object): Обьект содержащий настройки для приложения
        bot_settings (object): Обьект содержащий настройки для бота
        root_modules_settings (List[ModuleSettings]): Список состоящий из обьектов
        содержащих настройки для модулей

    Returns:
        LoggerRuntime: Склад логов
    """

    # Создание фабрики логгеров для приложения и бота
    app_factory: LoggerFactory = LoggerFactory(
        base_path=app_path.LOG_DIR,
        datefmt=log_format.DATE_FORMAT,
        format_log=log_format.LOG_FORMAT,
    )

    bot_factory: LoggerFactory = LoggerFactory(
        base_path=bot_path.LOG_DIR,
        datefmt=log_format.DATE_FORMAT,
        format_log=log_format.LOG_FORMAT,
    )

    # Добавление в хранилище фабрики логгеров логгеры бота, приложения,
    # корневых модулей

    storage.add(
        name=app_settings.SERVICE_NAME,
        data=app_factory.create(name=app_settings.SERVICE_NAME),
    )
    storage.add(
        name=bot_settings.SERVICE_NAME,
        data=bot_factory.create(name=bot_settings.SERVICE_NAME),
    )
    for settings in root_modules_settings:
        storage.add(
            name=settings.SERVICE_NAME,
            data=bot_factory.create(
                name=settings.SERVICE_NAME,
                subdir=settings.SERVICE_NAME,
            ),
        )

    LoggerRuntime.init(storage=storage)

    return LoggerRuntime


def create_app_context(
    bot_modules_root: str = DEFAULT_BOT_MODULES_ROOT,
) -> AppContext:
    """Создает контекст приложения."""

    app_settings = load_settings("app.settings")
    bot_settings = load_settings("app.bot.settings")
    app_path = load_app_paths("app.core.paths")
    bot_path = load_bot_paths("app.bot.core.paths")
    modules_settings = load_bot_root_modules_settings(DEFAULT_BOT_MODULES_ROOT)

    loggers = init_logging(
        app_path=app_path,
        app_settings=app_settings,
        bot_path=bot_path,
        bot_settings=bot_settings,
        root_modules_settings=modules_settings,
    )

    return AppContext(
        app_path=app_path,
        bot_path=bot_path,
        app_settings=app_settings,
        bot_settings=bot_settings,
        loggers=loggers,
        root_modules_settings=modules_settings,
    )
