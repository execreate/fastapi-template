import factory
from datetime import datetime


class TimeStampedFactory(factory.Factory):
    created_at = datetime.now()
    modified_at = datetime.now()
