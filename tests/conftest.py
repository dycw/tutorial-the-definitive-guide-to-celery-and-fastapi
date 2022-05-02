from collections.abc import Iterator

from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app


@fixture(scope="function")
def test_client() -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client
