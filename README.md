# FastAPI template

A simple starting point for your [FastAPI](https://fastapi.tiangolo.com) application.

## Features

1. UV for dependency management. Simply run `uv sync` to install get started, read more about UV
   at https://docs.astral.sh/uv/
2. Docker compose for local development and testing
3. SQLAlchemy for ORM (uses async engine) and Alembic for database migrations
4. Simple authentication for docs page
5. CRUD operations generic class with pagination
6. Support for API versioning (`https://api.yourdomain.com/v1/`)
7. Async testing suite with Pytest
8. [ClickStack](https://clickhouse.com/use-cases/observability) integration for telemetry

## Start coding

Just click on that green `Use this template` button to start coding. There is [a dummy app](app/api/v1/blog_post.py)
that
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

### Tests

Adapt the database connection string and run tests with:

```shell
ENVIRONMENT=test pytest
```

Use docker-compose to run your app:

```shell
docker compose up -d
```

### Auto-generated docs

If you run the code without any changes, you'll find the
[documentation page here](http://localhost:8001/docs). The default username is `docs_user`
and the password is `simple_password`.

### Telemetry

After you add new dependencies, run the following command to also add opentelemetry instruments:

```shell
uv add --group telemetry $(opentelemetry-bootstrap -a requirements)
```

This template uses [ClickStack](https://clickhouse.com/use-cases/observability).