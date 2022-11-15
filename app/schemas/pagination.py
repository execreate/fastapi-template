class LimitOffsetPaginationParams:
    def __init__(self, limit: int = 20, offset: int = 0):
        self.limit = limit
        self.offset = offset
