from sqlalchemy.orm import Session
from Repositories.models import Movie, Rate, User


class MovieRepository:
    def __init__(self, db_session:Session):
        self.db = db_session

    def get_movies (self) -> list[Movie]:
        return self.db.query(Movie).all()
