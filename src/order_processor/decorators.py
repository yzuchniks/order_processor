import asyncio
import functools
import logging

from constants import Retry

logger = logging.getLogger(__name__)


def retry(
    max_retries=Retry.MAX_RETRIES.value,
    delay=Retry.DELAY.value,
    exceptions=(Exception,),
):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    logger.error(
                        f"Ошибка при вызове {func.__name__}: {e}. "
                        f"Попытка {retries}/{max_retries}",
                        exc_info=True,
                    )
                    if retries >= max_retries:
                        logger.error(
                            f"Максимальное количество попыток "
                            f"({max_retries}) исчерпано."
                        )
                        raise
                    await asyncio.sleep(delay)

        return wrapper

    return decorator
