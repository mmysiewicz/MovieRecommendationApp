from Exceptions.Exceptions import ScoreOutOfRangeException
from Repositories.models import Movie, User
from Repositories.movie_repository import MovieRepository


class Service:
    def __init__(self, movie_repository: MovieRepository):
        self.repo = movie_repository
        self.user: User | None = None

    def get_all_movies(self) -> list[Movie]:
        movies = self.repo.get_movies()
        return movies

    def get_recommended_movies(self) -> list[Movie]:
        return []

    def password_check(self, login:str, password:str) -> User | None:
        user = self.repo.get_user_by_login(login)
        if user and user.Password == password:
            self.user = user
            return user
        return None

    def rate_movie(self, movie_id : int, score : int):
        if score not in range(1, 11):
            raise ScoreOutOfRangeException(score)
        try:
            self.repo.insert_update_rate(movie_id, self.user.Id, score)
        except Exception as e:
            print(e)
            self.repo.db.rollback()

