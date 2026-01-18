from pathlib import Path
from typing import List

from app.bot.core.bot import dp
from app.bot.core.paths import bot_path
from app.bot.core.bot import telegram_bot
from app.bot.settings import settings
from app.bot.core.middleware.errors import RouterErrorMiddleware
from app.app_utils.keyboards import get_total_buttons_reply_kb
from core.module_loader.loader import load_modules
from core.utils.filesistem import ensure_directories
from core.module_loader.register import register_module
from core.logging.api import get_loggers
from core.contracts.constants import DEFAULT_BOT_MODULES_ROOT


from aiogram import Dispatcher


async def setup_bot() -> Dispatcher:
    """Подключает все необходимые компоненты для работы бота."""

    logging_bot = get_loggers(name=settings.NAME_FOR_LOG_FOLDER)

    array_modules = load_modules(
        root_package=DEFAULT_BOT_MODULES_ROOT,
    )

    register_module(
        dp=dp,
        modules=array_modules,
        logging_data=logging_bot,
    )  # регестрируем модули

    list_path_to_temp_folder = [
        bot_path.TEMP_DIR / Path(m.settings.settings.NAME_FOR_TEMP_FOLDER)
        for m in array_modules
    ]  # получаем список из путей для папки temp

    ensure_directories(
        bot_path.TEMP_DIR,
        bot_path.STATIC_DIR,
        *list_path_to_temp_folder,
    )  # создает нужные пути

    root_modules = [m for m in array_modules if m.is_root]

    # Формируем клавиатуру для главного меню
    settings_modules = [m.settings.settings for m in array_modules]
    get_main_keyboards = get_total_buttons_reply_kb(
        list_text=[
            settings.MENU_REPLY_TEXT
            for settings in settings_modules
            if settings.SERVICE_NAME != "main"
        ],
        quantity_button=2,
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

    return get_main_keyboards, dp
