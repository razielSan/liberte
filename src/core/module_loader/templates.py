from typing import Dict, List


TEMPLATE_FILES: Dict[str, str] = {
    """__init__.py""": "# init for {name}\n",
    "router.py": """from pathlib import Path
from importlib import import_module
from core.logging.api import get_loggers
from .settings import settings

from aiogram import Router, Dispatcher
        
    
router: Router = Router(name=settings.SERVICE_NAME)

            
# Include sub router            
current_dir = Path(__file__).resolve().parent
handlers_path = current_dir / "handlers"
            
            
logging_data = get_loggers(name=settings.NAME_FOR_LOG_FOLDER)            
for file in handlers_path.glob("*.py"):
    if file.name == "__init__.py":
        continue

    module_name = f"{__package__}.handlers.{file.stem}"
    module = import_module(module_name)

    handler_router = getattr(module, "router", None)

    if handler_router:
        router.include_router(handler_router)
        logging_data.info_logger.info(
            "\\n[Auto] Sub router inculde into {}: {}".format(router, handler_router)
        )  
    """,
    "settings.py": """from pydantic import BaseModel


class ModuleSettings(BaseModel):
    SERVICE_NAME: str = "{name}"
    MENU_REPLY_TEXT: str = "{name}" 
    MENU_CALLBACK_TEXT: str = "{name}"
    MENU_CALLBACK_DATA: str = "{name}"
    NAME_FOR_LOG_FOLDER: str = "{log_name}"
    NAME_FOR_TEMP_FOLDER: str = "{temp_path}"
    ROOT_PACKAGE: str = "{root_package}"
    
settings: ModuleSettings = ModuleSettings()
    """,
    "response.py": """# Responses, strings, text for module {name}
from pathlib import Path

from core.module_loader.loader import get_child_modules_settings_inline_data
from app.app_utils.keyboards import get_total_buttons_inline_kb
from app.bot.core.paths import bot_path


inline_data = get_child_modules_settings_inline_data(
    module_path=bot_path.BOT_DIR / "modules" / Path("{path_to_module}"),
    root_package="{root_childes}"
)

get_keyboards_menu_buttons = get_total_buttons_inline_kb(
    list_inline_kb_data=inline_data, quantity_button=1
)
""",
    "extensions.py": "# Plug-in extensions are below",
}


TEMPLATE_DIRS: List[str] = [
    "api",
    "fsm",
    "services",
    "utils",
    "handlers",
    "keyboards",
    "childes",
]
