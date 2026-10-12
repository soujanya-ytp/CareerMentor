from app.db import sqlite_compat  # noqa: F401
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
