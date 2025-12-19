from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_database_url

engine = create_engine(get_database_url(), pool_pre_ping=True)


def init_db() -> None:
    from app.models.document import Document  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
