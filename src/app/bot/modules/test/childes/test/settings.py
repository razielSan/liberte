from pydantic import BaseModel


class ModuleSettings(BaseModel):
    SERVICE_NAME: str = "test.childes.test"
    MENU_REPLY_TEXT: str = "test.childes.test" 
    MENU_CALLBACK_TEXT: str = "test.childes.test"
    MENU_CALLBACK_DATA: str = "test.childes.test"
    SHOW_IN_MAIN_MENU: bool = True
    NAME_FOR_LOG_FOLDER: str = "test"
    NAME_FOR_TEMP_FOLDER: str = "test/childes/test"
    ROOT_PACKAGE: str = "app.bot.modules.test.childes.test"
    
settings: ModuleSettings = ModuleSettings()
    