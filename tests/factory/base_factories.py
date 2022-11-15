import factory
from datetime import datetime


class TimeStampedFactory(factory.Factory):
    id = factory.Faker("uuid4")
    created_at = datetime.now()
    modified_at = datetime.now()
