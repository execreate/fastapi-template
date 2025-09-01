import logging

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
