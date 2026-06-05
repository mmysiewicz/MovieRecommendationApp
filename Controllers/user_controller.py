from Repositories.models import User
from Repositories.movie_repository import MovieRepository
from Services.service import Service


class UserController:
    def __init__(self, repository: MovieRepository, service: Service):
        self.repo = repository
        self.service = service


    def login(self, login: str, password: str) -> User | None:
        return self.service.password_check(login, password)