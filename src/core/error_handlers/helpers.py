from typing import Callable, Optional, Union, Any, Dict
from asyncio import AbstractEventLoop, exceptions
import functools
import traceback
from logging import Logger
import importlib
from types import ModuleType

from core.response.response_data import LoggingData, ResponseData, Result, Error
from core.error_handlers.format import format_errors_message
from core.response.messages import messages


def ok(data: None) -> Result:
    return Result(
        ok=True,
        data=data,
    )


def fail(
    code: str,
    message: str,
    details=None,
) -> Result:
    return Result(
        ok=False,
        error=Error(
            code=code,
            message=message,
            detatails=details,
        ),
    )


async def run_safe_inf_executror(
    loop: AbstractEventLoop,
    func: Callable,
    *args,
    logging_data: Optional[LoggingData] = None,
    **kwargs,
) -> Union[Any, ResponseData]:
    """
    Отлавливает все возможные ошибки для переданной синхронной функции.

    При ошибке в ходе выполнения функции выкидывает обьект класса ResponseData

    Args:
        loop (AbstractEventLoop): цикл событий
        func (Callable): функция для цикла
        logging_data (Optional[LoggingData], optional): обьект класс
        LoggingData содержащий логгер и имя роутера. None по умолчанию

    Returns:
        Union[Any, NetworkResponseData]: Возвращает loop.run_in_executor
    """
    try:
        return await loop.run_in_executor(
            None,
            functools.partial(
                func,
                *args,
                **kwargs,
            ),
        )
    except exceptions.CancelledError:
        print("Остановка работы процесса пользователем")
        return ResponseData(
            message="Остановка работы процесса пользователем",
            error=None,
        )

    except Exception as err:
        if logging_data:
            logging_data.error_logger.exception(
                format_errors_message(
                    name_router=logging_data.router_name,
                    status=0,
                    method="<unknown>",
                    url="<unknown>",
                    error_text=err,
                    function_name=func.__name__,
                )
            )
        else:
            print(err)
        return ResponseData(
            error=messages.SERVER_ERROR,
            message=None,
        )


def safe_import(
    module_path: str,
    error_logger: Logger = None,
) -> Result:
    """
    Безопасный импорт модуля.

    Возвращает модуль или None если произошла ошибка.
    """
    try:
        return ok(data=importlib.import_module(module_path))
    except Exception as err:
        if error_logger:
            error_logger.error(
                f"[IMPORT ERROR] Модуль {module_path} не загрузился\n"
                f"{err}\n{traceback.format_exc()}"
            )

        return fail(
            code="IMPORT ERROR",
            message=f"Модуль {module_path} не загрузился\n{err}",
        )
