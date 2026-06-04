from Repositories.movie_repository import MovieRepository
from Services.movie_service import MovieService


class MovieController:
    def __init__(self, movie_repository: MovieRepository, movie_service: MovieService):
        self.repo = movie_repository
        self.service = movie_service

    def get_data(self):
        movies = self.service.get_all_movies()
        return {"filmy" : movies}