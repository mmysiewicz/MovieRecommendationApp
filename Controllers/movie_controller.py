from Repositories.movie_repository import MovieRepository


class MovieController:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository
