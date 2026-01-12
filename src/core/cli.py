from typing import List
from pathlib import Path
import sys

from core.scripts.bot.create_module import creates_new_modules_via_the_command_line
from core.scripts.bot.remove_module import remove_module
from core.paths.paths import SRC_DIR


# MODULES_ROOT: Path = APP_DIR / "bot" / "modules"


def main() -> None:
    """
    Команды для командной строки.

    cli add-module <путь> <путь> - Создание модулей
    cli remove-module <путь> - Удаление модуля
    """

    list_sys_argv: List[str] = sys.argv

    if len(list_sys_argv) < 2:
        print(
            "Использование:\n\npython manage.py add-module"
            " <name module>\npython manage.py remove-module <name module>"
        )
        sys.exit()

    command: str = list_sys_argv[1]
    if command == "add-module":
        if len(list_sys_argv) < 3:
            print(
                "Укажите имя модуля.Дочерний модуль должен быть "
                "разделен '.'\ncli add-module <name module>"
                "\ncli add-module test.data.test"
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
                "Укажите путь до модуля.Дочерний модуль должен быть "
                "разделен 'childes'\ncli add-module <путь>"
                "\ncli add-module test/childes/data"
            )
            exit()
        elif len(list_sys_argv) >= 4:
            print("За раз можно удалить только один модуль\ncli remove-module <путь>")
            exit()
        else:
            # LOG_PATH: Path = APP_DIR / "logs" / "bot"
            # TEMP_PATH: Path = APP_DIR / "bot" / "temp"
            # MODULES_PATH: Path = MODULES_ROOT
            remove_module(
                name_module=list_sys_argv[2],
                log_path=1,
                temp_path=2,
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
