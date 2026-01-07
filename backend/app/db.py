from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .config import DB_PATH, ensure_dirs


class Base(DeclarativeBase):
    pass


def get_engine():
    ensure_dirs()
    return create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})


engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
