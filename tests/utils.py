import asyncio
import logging
from typing import Any, Coroutine, TypeVar


logger = logging.getLogger(__name__)


def dicts_are_equal(d1: dict, d2: dict, for_keys: set):
    for k, v1 in d1.items():
        if (for_keys is None or k in for_keys) and (k not in d2 or d2[k] != v1):
            logger.warning(f"{v1} is not equal to {d2[k]}")
            return False

    for k, v2 in d2.items():
        if (for_keys is None or k in for_keys) and (k not in d1 or d1[k] != v2):
            logger.warning(f"{v2} is not equal to {d1[k]}")
            return False

    return True


_T = TypeVar("_T")

def check_event_loop():
    try:
        asyncio.get_event_loop_policy().get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)


def run_sync(co: Coroutine[Any, Any, _T]) -> _T:
    check_event_loop()
    loop = asyncio.get_event_loop_policy().get_event_loop()
    return loop.run_until_complete(co)
