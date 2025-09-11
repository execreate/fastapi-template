#!/bin/bash

set -Eeuo pipefail

# Let the DB start
opentelemetry-instrument python backend_pre_start.py

alembic upgrade head

exec "$@"
