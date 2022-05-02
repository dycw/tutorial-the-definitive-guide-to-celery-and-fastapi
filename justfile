build:
  DOCKER_BUILDKIT=1 docker build -t=docker-template --target=production .

lint:
  DOCKER_BUILDKIT=1 docker build -t=docker-template --target=lint .

local:
  poetry run uvicorn --host=localhost --port=8000 --reload main:app

test:
  DOCKER_BUILDKIT=1 docker build -t=docker-template --target=test .

#### commands #################################################################

worker:
  celery -A main.celery worker --loglevel=info

flower:
  celery -A main.celery flower --port=5555

alembic-rev:
  alembic revision --autogenerate

alembic-up:
  alembic upgrade head
