from pathlib import Path
from collections.abc import Generator

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from app.utils.config import settings

ALEMBIC_INI_PATH = Path(__file__).resolve().parents[2] / "alembic.ini"
MAIN_DATABASE_URL = settings.database_url


def get_database_url() -> str:
    return MAIN_DATABASE_URL


def get_database_url_for_logging() -> str:
    return make_url(MAIN_DATABASE_URL).render_as_string(hide_password=True)


def get_engine_options(database_url: str | None = None) -> dict[str, object]:
    resolved_url = database_url or get_database_url()
    engine_options: dict[str, object] = {"pool_pre_ping": True}

    if resolved_url.startswith("sqlite"):
        engine_options["connect_args"] = {"check_same_thread": False}

    return engine_options


engine = create_engine(get_database_url(), **get_engine_options())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    alembic_config = Config(str(ALEMBIC_INI_PATH))
    alembic_config.set_main_option("sqlalchemy.url", get_database_url().replace("%", "%%"))
    command.upgrade(alembic_config, "head")


def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
