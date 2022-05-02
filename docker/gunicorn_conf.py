from json import dumps  # noqa: INP001
from logging import INFO
from logging import basicConfig
from logging import info
from os import cpu_count
from os import getenv
from sys import stdout


# From: https://bit.ly/3F2I0hH


basicConfig(level=INFO, stream=stdout)


workers_per_core_str = getenv("WORKERS_PER_CORE", "1")
web_concurrency_str = getenv("WEB_CONCURRENCY", None)
host = getenv("HOST", "0.0.0.0")  # noqa: S104
port = getenv("PORT", "8000")
bind_env = getenv("BIND", None)
use_loglevel = getenv("LOG_LEVEL", "info")
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

if (cores := cpu_count()) is None:
    raise ValueError(f"{cores=}")
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    if (web_concurrency := int(web_concurrency_str)) <= 0:
        raise ValueError(f"{web_concurrency=}")
else:
    web_concurrency = max(int(default_web_concurrency), 2)

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
keepalive = 120
errorlog = "-"

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "host": host,
    "port": port,
}
info(dumps(log_data))
