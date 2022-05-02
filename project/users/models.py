from typing import Any

from beartype import beartype
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from project.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)

    @beartype
    def __init__(
        self, username: str, email: str, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__()
        self.username = username
        self.email = email
