from typing import Optional, Any, Dict
from dataclasses import dataclass
from logging import Logger

from pydantic import BaseModel


class Error(BaseModel):
    code: str
    message: str
    detatails: Optional[Any] = None


class Result(BaseModel):
    ok: bool
    data: Optional[Any] = None
    error: Optional[Error] = None


class NetworkResponseData(BaseModel):
    """Модель для возвращаения сетевых ответов."""

    error: Optional[str] = None
    message: Optional[Any] = None
    url: Optional[str] = None
    status: Optional[int] = None
    method: Optional[str] = None
    headers: Optional[Dict] = None


class ResponseData(BaseModel):
    """Модель для возвращаения ответов."""

    error: Optional[str] = None
    message: Optional[Any] = None


@dataclass
class LoggingData:
    """Модель для возврата логгеров."""

    info_logger: Logger
    warning_logger: Logger
    error_logger: Logger
    critical_logger: Logger
    router_name: str


@dataclass
class InlineKeyboardData:
    """Модель для инлайн клавиатуры."""

    text: str
    callback_data: str
    resize_keyboard: bool = True
