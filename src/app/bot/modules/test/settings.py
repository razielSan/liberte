from pydantic import BaseModel


class ModuleSettings(BaseModel):
    SERVICE_NAME: str = "test"
    MENU_REPLY_TEXT: str = "test" 
    MENU_CALLBACK_TEXT: str = "test"
    MENU_CALLBACK_DATA: str = "test"
    SHOW_IN_MAIN_MENU: bool = True
    NAME_FOR_LOG_FOLDER: str = "test"
    NAME_FOR_TEMP_FOLDER: str = "test"
    ROOT_PACKAGE: str = "app.bot.modules.test"
    
settings: ModuleSettings = ModuleSettings()
    