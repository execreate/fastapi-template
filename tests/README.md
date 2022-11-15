# Testing your app

Since the app uses async style, the testing setup is completely asynchronous too. It makes use of `AsyncClient`
from [httpx package](https://www.python-httpx.org).

[Provided fixtures](tests/conftest.py) override the dependencies of your FastAPI application to make sure
the unit test function and your app use the same database session - this way you can avoid committing your
changes to the db session.

Please don't forget to export `ENVIRONMENT=test` into your environment to avoid your API functions from
committing changes to the database when using the [CRUD factory](app/db/crud/base.py).  
