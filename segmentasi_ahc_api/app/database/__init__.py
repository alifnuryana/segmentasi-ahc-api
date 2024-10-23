from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

engine = create_engine(
    "sqlite:///database.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
