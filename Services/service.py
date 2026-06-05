from Exceptions.exceptions import ScoreOutOfRangeException
from Repositories.models import Movie, User
from Repositories.movie_repository import MovieRepository
from Services.recommender import Recommender


class Service:
    def __init__(self, movie_repository: MovieRepository):
        self.repo = movie_repository
        self.user: User | None = None

    def get_all_movies(self) -> list[Movie]:
        movies = self.repo.get_movies()
        return movies

    def get_recommended_movies(self, count : int = 5 ) -> list[Movie]:
        movies = self.get_all_movies()
        recommender = Recommender(movies)

        recommendations_generator = recommender.create_recommendations(self.user)

        top = []
        for i in range(count):
            try:
                top.append(next(recommendations_generator))
            except StopIteration:
                break
        return top



    def password_check(self, login:str, password:str) -> User | None:
        user = self.repo.get_user_by_login(login, password)
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

    def get_director_for_movie(self, movie_id: int) -> str:
        return self.repo.get_director_for_movie(movie_id)

