from core.logging.logging import LoggerStorage
from core.logging.format import log_format
from core.logging.logging import setup_bot_logging
from app.bot.settings import BotSettings
from app.bot.core.paths import bot_path

bot_settings: BotSettings = BotSettings()

logging_data: LoggerStorage = LoggerStorage()


bot_info_logger, bot_warning_logger, bot_error_logger = setup_bot_logging(
    log_name=bot_settings.BOT_NAME,
    base_path=bot_path.LOG_DIR,
    base_dir=True,
    log_format=log_format.LOG_FORMAT,
    date_format=log_format.DATE_FORMAT,
)
