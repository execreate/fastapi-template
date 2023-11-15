import factory
from datetime import datetime


class TimeStampedFactory(factory.Factory):
    created_at = datetime.now()
    updated_at = datetime.now()
