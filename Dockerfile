# syntax=docker/dockerfile:1

# https://bit.ly/374AGW9 - Lighten your Python image with Docker multi-stage builds
# https://bit.ly/39upBi5 - Fast Docker Builds With Caching (Not Only) For Python
# https://bit.ly/3FcBF3m - Poetry managed Python FastAPI application with Docker multi-stage builds

# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

#### python-base ##############################################################
# Creating a python base with shared environment variables
FROM python:3.10.4-slim as python-base
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_NO_CACHE_DIR=off \
  POETRY_HOME="/opt/poetry" \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

#### builder-base #############################################################
# builder-base is used to build dependencies
FROM python-base as builder-base
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  curl \
  build-essential

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.13
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev  # respects

#### development ##############################################################
# 'development' stage installs all dev deps and can be used to develop code.
# For example using docker-compose to mount local volume under /app
FROM python-base as development
ENV FASTAPI_ENV=development

# Copying poetry and venv into image
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Copying in our entrypoint
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# venv already has runtime deps installed we get a quicker install
WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR /app
COPY . .

EXPOSE 8000
ENTRYPOINT /entrypoint.sh $0 $@
CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--port=8000", "main:app"]

#### lint #####################################################################
# 'lint' stage runs black and isort
# running in check mode means build will fail if any linting errors occur
FROM development AS lint
RUN black --check -q app tests
RUN isort --check app tests
CMD ["tail", "-f", "/dev/null"]

#### test #####################################################################
# 'test' stage runs our unit tests with pytest and
# coverage.  Build will fail if test coverage is under 95%
FROM development AS test
RUN coverage run --rcfile ./pyproject.toml -m pytest ./tests
RUN coverage report --fail-under 95

#### production ###############################################################
# 'production' stage uses the clean 'python-base' stage and copyies
# in only our runtime deps that were installed in the 'builder-base'
FROM python-base as production
ENV FASTAPI_ENV=production

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY ./docker/gunicorn_conf.py /gunicorn_conf.py

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./app /app
WORKDIR /app

ENTRYPOINT /entrypoint.sh $0 $@
CMD ["gunicorn", "--worker-class uvicorn.workers.UvicornWorker", \
  "--config /gunicorn_conf.py", "main:app"]
