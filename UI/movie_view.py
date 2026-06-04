import customtkinter as ctk
from Controllers.movie_controller import MovieController
from Repositories.models import Movie
from UI.tile import Tile


class MovieView(ctk.CTk):
    def __init__(self, movie_controller : MovieController):
        super().__init__()
        self.controller = movie_controller

        self.title("Movie recommender")
        self.geometry("800x600")
        self.resizable(True, True)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.label = ctk.CTkLabel(self, text="Filmy", font=ctk.CTkFont(family="Roboto", size=25, weight="bold"))
        self.label.pack(pady=20)

        self.scrollable_frame = ctk.CTkFrame(self, width=600, height=400)
        self.scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, pad=20)

        self.display_movies()

    def display_movies(self):
        data = self.controller.get_data()
        #movies = data["filmy"]

        # 1. Zabezpieczenie: Jeśli data jest None, przypisz pusty słownik
        if data is None:
            data = {"filmy": []}

        # 2. Bezpieczne pobranie listy (jeśli klucza nie ma, .get() da pustą listę [])
        movies = data.get("filmy", [])

        # 3. Jeśli lista filmów jest pusta, wyświetlamy ładny komunikat w UI
        if not movies:
            no_movies_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Brak filmów w bazie danych. Dodaj jakieś pozycje!",
                font=ctk.CTkFont(family="Roboto", size=16)
            )
            no_movies_label.pack(pady=50)
            return  # Przerywamy wykonywanie metody, nie ma po czym iterować


        for i, movie in enumerate(movies):
            row = i//4
            col = i%4

            tile = Tile(self.scrollable_frame, movie, on_click=self.on_select_tile)

            tile.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

    def on_select_tile(self, movie : Movie):
        print(f"Kliknięto {movie.Title}")