import customtkinter as ctk
from Controllers.movie_controller import MovieController
from Repositories.models import Movie, User
from UI.tile import Tile


class MovieView(ctk.CTkToplevel):
    def __init__(self, movie_controller : MovieController, user : User):
        super().__init__()
        self.controller = movie_controller
        self.user = user

        self.protocol("WM_DELETE_WINDOW", self._handle_close)
        self.title("Movie recommender")
        self.geometry("800x600")
        self.resizable(True, True)

        self.label = ctk.CTkLabel(self, text="Filmy", font=ctk.CTkFont(family="Roboto", size=20, weight="bold"))
        self.label.pack(pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, pad=20)


        self.recommendation_label = ctk.CTkLabel(self, text="Rekomendowane", font=ctk.CTkFont(family="Roboto", size=20, weight="bold"))
        self.recommendation_label.pack(pady=20)

        self.scrollable_bottom_frame = ctk.CTkScrollableFrame(self, width=600, height=300, orientation= "horizontal")
        self.scrollable_bottom_frame.pack(pady=10, padx=20, fill="both", expand=False)

        self.after(100, self._load_data)

    def _load_data(self):
        try:
            self.display_movies()
            self.display_recommended_movies()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def display_movies(self):
        movies = self.controller.get_data()

        if movies is None:
            movies = []

        if len(movies) == 0:
            empty_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Brak filmów w bazie",
                font=ctk.CTkFont(family="Roboto", size=15)
            )
            empty_label.grid(pady=50)
            return


        for i, movie in enumerate(movies):
            row = i//4
            col = i%4

            tile = Tile(self.scrollable_frame, movie, on_click=self.on_select_tile)

            tile.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

    def display_recommended_movies(self):
        movies = self.controller.get_recommended_movies()

        if movies is None:
            movies = []

        if len(movies) == 0:
            empty_label = ctk.CTkLabel(
                self.scrollable_bottom_frame,
                text="Brak filmów w bazie",
                font=ctk.CTkFont(family="Roboto", size=15)
            )
            empty_label.grid(pady=50)
            return


        for movie in movies:
            tile = Tile(self.scrollable_bottom_frame, movie, on_click=self.on_select_tile)
            tile.pack(side="left", padx=10, pady=5)

    def on_select_tile(self, movie : Movie):
        print(f"Kliknięto {movie.Title}")

    def _handle_close(self):
        self.quit()
        self.destroy()