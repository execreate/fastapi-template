#!/bin/bash

set -Eeuo pipefail

# Let the DB start
python3 backend_pre_start.py

exec "$@"
