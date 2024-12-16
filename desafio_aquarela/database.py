from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from desafio_aquarela.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    """
    Yields:
        sqlalchemy.orm.Session: the database session.
    """
    with Session(engine) as session:
        yield session
