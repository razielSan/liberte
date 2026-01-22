from pathlib import Path
from typing import List
import traceback

from app.bot.core.bot import dp
from app.bot.core.paths import bot_path
from app.bot.core.bot import telegram_bot
from app.bot.settings import settings
from app.bot.core.middleware.errors import RouterErrorMiddleware
from app.app_utils.keyboards import get_total_buttons_reply_kb
from core.module_loader.runtime.loader import load_modules
from core.utils.filesistem import ensure_directories
from core.module_loader.runtime.register import register_module
from core.logging.api import get_loggers
from core.contracts.constants import DEFAULT_BOT_MODULES_ROOT
from core.error_handlers.helpers import ok, fail
from core.response.response_data import Result
from core.error_handlers.format import format_errors_message


async def setup_bot() -> Result:
    """Подключает все необходимые компоненты для работы бота."""
    try:
        logging_bot = get_loggers(name=settings.NAME_FOR_LOG_FOLDER)

        result_load_modules = load_modules(
            root_package=DEFAULT_BOT_MODULES_ROOT,
        )
        if not result_load_modules.ok:
            return result_load_modules

        array_modules = result_load_modules.data

        register_module(
            dp=dp,
            modules=array_modules,
            logging_data=logging_bot,
        )  # регестрируем модули

        list_path_to_temp_folder = [
            bot_path.TEMP_DIR / Path(m.settings.settings.NAME_FOR_TEMP_FOLDER)
            for m in array_modules
        ]  # получаем список из путей для папки temp

        result_directory = ensure_directories(
            bot_path.TEMP_DIR,
            bot_path.STATIC_DIR,
            *list_path_to_temp_folder,
            logging_data=logging_bot,
        )  # создает нужные пути
        if not result_directory.ok:
            return result_directory

        root_modules = [m for m in array_modules if m.is_root]

        # Формируем клавиатуру для главного меню
        settings_modules = [
            m.settings.settings.MENU_REPLY_TEXT
            for m in root_modules
            if m.settings.settings.SHOW_IN_MAIN_MENU
        ]
        get_main_keyboards = None
        if len(settings_modules) == 0:
            logging_bot.warning_logger.warning(
                "Клавиатура для "
                "главного меню не была создана:\nПодключен только главный модуль"
                " или остальные модули скрыты"
            )
        else:
            get_main_keyboards = get_total_buttons_reply_kb(
                list_text=settings_modules,
                quantity_button=2,
            )
            buttons: str = ", ".join(settings_modules)
            logging_bot.info_logger.info(
                f"Подключена клавиатура главного меню:\nПодключены кнопки - {buttons}"
            )

        await telegram_bot.set_my_commands(
            commands=settings.LIST_BOT_COMMANDS  # Добавляет команды боту
        )  # Добавляет команды боту
        await telegram_bot.delete_webhook(
            drop_pending_updates=True
        )  # Игнорирует все присланные сообщение пока бот не работал

        for model in root_modules:
            # получаем  логгеры
            logging_data = get_loggers(
                name=model.settings.settings.NAME_FOR_LOG_FOLDER,
            )

            # Подключаем middleware
            model.router.router.message.middleware(
                RouterErrorMiddleware(
                    logger=logging_data.error_logger,
                )
            )
            model.router.router.callback_query.middleware(
                RouterErrorMiddleware(logger=logging_data.error_logger)
            )

            logging_bot.info_logger.info(
                f"Middleware для {logging_data.router_name} подключен"
            )

        return ok(data=(get_main_keyboards, dp))
    except Exception as err:
        logging_bot.error_logger.error(
            msg=format_errors_message(
                name_router=logging_bot.router_name,
                function_name=setup_bot.__name__,
                error_text=f"Критическая ошибка в работе startup\n{traceback.format_exc()}",
            )
        )
        return fail(
            code="STARTUP FAIL",
            message=f"Критическая ошибка в работе startup - {err}",
            details=str(traceback.format_exc()),
        )
