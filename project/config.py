from dataclasses import dataclass
from dataclasses import field
from functools import lru_cache
from os import getenv
from pathlib import Path
from typing import Any


@dataclass
class BaseConfig:
    BASE_DIR: Path = Path(__file__).parent.parent
    DATABASE_URL: str = getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3"
    )
    DATABASE_CONNECT_DICT: dict[str, Any] = field(default_factory=dict)


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings() -> BaseConfig:
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    config_name = getenv("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
