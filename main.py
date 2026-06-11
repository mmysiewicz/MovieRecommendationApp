from sqlalchemy.engine import URL
from Repositories.connection import DatabaseManager
from Repositories.json_data_exporter import JsonDataExporter
from Repositories.models import Base, User
from Repositories.repository import MovieRepository
from Services.service import Service
from Controllers.movie_controller import MovieController
from Controllers.user_controller import UserController
from UI.movie_view import MovieView
from UI.login_view import LoginView

CONNECTION_STRING = URL.create(
    "mssql+pyodbc", query={"odbc_connect": "Driver={ODBC Driver 18 for SQL Server};Server=.\\SQLEXPRESS;Database=PythonDB;Trusted_Connection=yes;TrustServerCertificate=yes;"})


def launch_app(movie_controller: MovieController, logged_user: User):
    main_app = MovieView(movie_controller, user=logged_user)
    main_app.mainloop()

def main():

    database_manager = DatabaseManager(CONNECTION_STRING)
    Base.metadata.create_all(bind = database_manager._engine)
    session = database_manager.get_session()

    try:
        movie_repository = MovieRepository(session)
        movie_service = Service(movie_repository)

        movie_controller = MovieController(movie_repository, movie_service)
        user_controller = UserController(movie_repository, movie_service)

        login_app = LoginView(user_controller, on_login_succeed = lambda user: launch_app(movie_controller, user))
        login_app.mainloop()

    except Exception as e:
        print(e)
    finally:
        rates = movie_repository.get_rates()
        session.close()
        JsonDataExporter.export_rates(rates, "rates.json")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program został zamknięty.")