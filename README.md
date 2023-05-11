# FastAPI template

A simple starting point for your [FastAPI](https://fastapi.tiangolo.com) application.

## Features

1. Pipenv for dependency management. Simply run `pipenv install --dev` to install get started.
2. Docker compose for local development and testing
3. SQLAlchemy for ORM (uses async engine) and Alembic for database migrations
4. Simple authentication for docs page
5. CRUD operations generic class with pagination
6. Support for API versioning (`https://api.yourdomain.com/v1/`)
7. Async testing suite with Pytest

## Start coding

Just click on that green `Use this template` button to start coding. There is [a dummy app](app/api/v1/blog_post.py) that
is already implemented for you so that you can quickly learn how to use the [CRUD factory](app/db/crud/base.py).

Make sure to mark the `app/` folder as source in your IDE otherwise you'll get import errors.
And since all your code (except tests) lives inside `app/` folder, you should import modules like this:
```python
from core.config import settings
```

and NOT like this:
```python
# this will throw an error!
from app.core.config import settings
```

### Develop

The following command will run a PostgreSQL database on your docker engine:
```shell
docker compose -f docker-compose-local.yml up -d
```
so that you can do
```shell
cd app; uvicorn main:app
```
or
```shell
ENVIRONMENT=test pytest
```

If you just want to build a docker container with your app and run it, just run:
```shell
docker compose up -d
```

### Auto-generated docs

If you run the code without any changes, you'll find the
[documentation page here](http://localhost:8001/docs). The default username is `docs_user`
and the password is `simple_password`.
