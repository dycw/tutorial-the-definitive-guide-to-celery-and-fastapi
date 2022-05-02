#!/usr/bin/env bash
# shellcheck source=/dev/null

set -e

# activate our virtual environment here
source /opt/pysetup/.venv/bin/activate

# You can put other setup logic here

# Evaluating passed command:
exec "$@"
