from pydantic import BaseModel


class AppSettings(BaseModel):
    """Общие настроцки для всего приложения."""

    BOT_ROOT_NAME: str = "root_bot"