from typing import Annotated

from fastapi import Depends


class LimitOffsetPaginationParams:
    def __init__(self, limit: int = 20, offset: int = 0):
        self.limit = limit
        self.offset = offset


PaginationDep = Annotated[
    LimitOffsetPaginationParams, Depends(LimitOffsetPaginationParams)
]
