from Repositories.models import Movie
from Repositories.movie_repository import MovieRepository


class MovieService:
    def __init__(self, movie_repository: MovieRepository):
        self.repo = movie_repository

    def get_all_movies(self) -> list[Movie]:
        movies = self.repo.get_movies()
        return movies

    def get_recommended_movies(self) -> list[Movie]:
        return list