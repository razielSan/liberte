from app.settings import AppSettings
from core.logging.logging import setup_bot_logging
from app.core.paths import app_path
from core.logging.format import log_format

# Настройки всего приложения
app_settings: AppSettings = AppSettings()


# логгеры приложения
root_info_logger, root_warning_logger, root_error_logger = setup_bot_logging(
    log_name=app_settings.BOT_ROOT_NAME,
    base_path=app_path.LOG_DIR,
    date_format=log_format.DATE_FORMAT,
    log_format=log_format.LOG_FORMAT,
    base_dir=True,
)
