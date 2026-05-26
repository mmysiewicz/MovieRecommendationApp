from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class DatabaseManager:
    def __init__(self, connection_string:str):
        self._engine = create_engine(connection_string)
        self._session_factory = sessionmaker(
            bind=self._engine,
            autoflush=True,
            autocommit=False)

    def get_session(self) -> Session:
        return self._session_factory()