import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def _url_sqlalchemy() -> str:
    return os.environ["DATABASE_URL"].replace(
        "postgresql://", "postgresql+psycopg://", 1
    )


engine = create_engine(_url_sqlalchemy())

SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)