Generic single-database configuration.

Generate new migrations with:

```shell
cd app

alembic revision --autogenerate -m "message"
```

Run migrations with:

```shell
alembic upgrade head
```

Read more about Alembic at https://alembic.sqlalchemy.org/en/latest/.