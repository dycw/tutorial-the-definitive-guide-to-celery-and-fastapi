build:
  DOCKER_BUILDKIT=1 docker build -t=docker-template --target=production .

lint:
  DOCKER_BUILDKIT=1 docker build -t=docker-template --target=lint .

local:
  poetry run uvicorn --host=localhost --port=8000 --reload app.main:app

test:
  DOCKER_BUILDKIT=1 docker build -t=docker-template --target=test .
