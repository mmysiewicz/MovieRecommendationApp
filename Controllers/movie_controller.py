from Exceptions.Exceptions import ScoreOutOfRangeException
from Repositories.movie_repository import MovieRepository
from Services.service import Service


class MovieController:
    def __init__(self, movie_repository: MovieRepository, service: Service):
        self.repo = movie_repository
        self.service = service

    def get_data(self) -> list:
        movies = self.service.get_all_movies()
        return movies

    def get_recommended_movies(self) -> list:
        movies = self.service.get_recommended_movies()
        return movies

    def rate_movie(self, movie_id: int, score: int):
        try:
            self.service.rate_movie(movie_id, score)
        except ScoreOutOfRangeException as e:
            print(e)