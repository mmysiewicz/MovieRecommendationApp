from sqlalchemy.orm import Session, joinedload
from Repositories.models import Movie, Rate, User, Person, MoviePerson, Role
from Services.decorators import transaction_check


class MovieRepository:
    def __init__(self, db_session:Session):
        self.db = db_session

    def get_movies (self) -> list[Movie]:
        return self.db.query(Movie).all()

    def get_rates (self) -> list[Rate]:
        return self.db.query(Rate).options(
            joinedload(Rate.Movie),
            joinedload(Rate.User)
        ).all()

    def get_user_by_login(self, login : str, password: str) -> User | None:
        return self.db.query(User).filter(User.Login == login, User.Password == password).first()

    @transaction_check
    def insert_update_rate(self, movie_id : int , user_id:int , score:int):

        exist_rate = self.db.query(Rate).filter(
            Rate.Movie_Id==movie_id,
            Rate.User_Id==user_id
        ).first()

        if exist_rate:
            exist_rate.score = score
        else:
            rate = Rate(
                Movie_Id=movie_id,
                User_Id=user_id,
                Score=score
            )
            self.db.add(rate)

        self.db.commit()

    def get_director_for_movie(self, movie_id : int) -> str:

        director = (self.db.query(Person.Firstname, Person.Surname)
                    .join(MoviePerson, MoviePerson.Person_id == Person.Id)
                    .join(Role, Role.Id == MoviePerson.Role_id)
                    .filter(MoviePerson.Movie_Id==movie_id)
                    .filter(Role.Name=="Director")
                    .first())

        if director:
            return f"{director.Firstname} {director.Surname}"
        return ""




