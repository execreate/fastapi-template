from datetime import datetime

import factory


class TimeStampedFactory(factory.Factory):
    created_at = datetime.now()
    updated_at = datetime.now()
