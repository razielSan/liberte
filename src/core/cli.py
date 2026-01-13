from typing import List
from pathlib import Path
import sys

from core.scripts.bot.create_module import creates_new_modules_via_the_command_line
from core.scripts.bot.remove_module import remove_module
from core.paths.paths import SRC_DIR
from core.context import load_bot_paths


def main() -> None:
    """
    Команды для командной строки.

    cli add-module <путь>- Создание модулей
    cli remove-module <путь> - Удаление модуля
    """

    list_sys_argv: List[str] = sys.argv

    if len(list_sys_argv) < 2:
        print(
            "-----\nИспользование:\n\ncli add-module "
            "<name module> - Создание модуля\n"
            "cli remove-module <name module> - Удаление модуля\n-----"
        )
        sys.exit()

    command: str = list_sys_argv[1]

    bot_path = load_bot_paths(bot_core="app.bot.core.paths")

    if command == "add-module":
        if len(list_sys_argv) < 3:
            print(
                "-----\nУкажите имя модуля.\n\nДочерний модуль должен быть "
                "разделен '.'\n\nПример:\nсli add-module test.data.test\n-----"
            )
            exit()
        else:
            print("Идет создание модулей...")
            creates_new_modules_via_the_command_line(
                root_dir=SRC_DIR,
                module_name=list_sys_argv[2],
                root_package="app.bot.modules",
            )
    elif command == "remove-module":
        if len(list_sys_argv) < 3:
            print(
                "-----\nУкажите путь до модуля.\n\nДочерний модуль должен быть "
                "разделен '.'\n\nПример:\n"
                "\ncli remove-module test.data\n-----"
            )
            exit()
        elif len(list_sys_argv) >= 4:
            print(
                "-----\nЗа раз можно удалить только один модуль\n\n"
                "Пример:\ncli remove-module test.test\n-----"
            )
            exit()
        else:

            remove_module(
                name_module=list_sys_argv[2],
                log_path=1,
                temp_path=bot_path.TEMP_DIR,
                root_package="app.bot.modules",
                root_dir=SRC_DIR,
            )
    elif command == "help":
        print(
            """Доступные команды:
              
cli add-module <путь> <путь> - Создание модулей
cli remove-module <путь> - Удаление модуля 
"""
        )
    else:
        print("Неизвестная команда\n\npython manage.py help - Основные команды")
