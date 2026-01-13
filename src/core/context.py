from pathlib import Path
import importlib
from typing import Protocol


class BotPathProtocol(Protocol):
    BOT_DIR: Path
    TEMP_DIR: Path
    LOG_DIR: Path
    STATIC_DIR: Path


def load_bot_paths(bot_core: str) -> BotPathProtocol:
    module = importlib.import_module(bot_core)
    if not hasattr(module, "bot_path"):
        raise RuntimeError("bot path not found")
    return module.bot_path
