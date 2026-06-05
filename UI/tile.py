import os
import customtkinter as ctk
from Exceptions.exceptions import ImageLoadException
from PIL import Image



class Tile(ctk.CTkFrame):
    def __init__(self, master, movie, on_click):
        super().__init__(master, width=100, height=300, cursor="hand2",
                         fg_color=("#EAEAEA", "#2B2B2B"))
        self.movie = movie
        self.on_click = on_click
        self.widgets =[]

        self.grid_propagate(False)
        self.pack_propagate(False)

        try:
            self._display_image()
        except ImageLoadException as e:
            print(e)

        self._click_event()


    def _display_image(self):

        if self.movie.poster_path is not None and os.path.exists(self.movie.poster_path):
            try:
                image = Image.open(self.movie.poster_path)
                ctkinter = ctk.CTkImage(light_image=image, dark_image=image, size=(200, 300))

                self.widget = ctk.CTkLabel(self, image=ctkinter, text="")
                self.widget.pack(pady=10, padx=10)
                self.widgets.append(self.widget)


            except Exception as e:
                self._display_title(self.movie.Title)
                raise ImageLoadException(
                   "Plik ma niepoprawny format lub jest uszkodzony",
                   self.movie.Title,
                   self.movie.poster_path)

        else:
            self._display_title(self.movie.Title)
            raise ImageLoadException(
                "Plik nie istnieje",
                self.movie.Title,
                self.movie.poster_path)

    def _display_title(self, text):
        self.widget = ctk.CTkLabel(self, text=text, font = ctk.CTkFont(family="Roboto", size=20))
        self.widget.pack(pady=100, padx=10, fill="both", expand=True)

    def _display_details(self):
        self._clear_tile()
        self.unbind("<Button-1>")

        title_label = ctk.CTkLabel(self, text=self.movie.Title,
                     font = ctk.CTkFont(family="Roboto", size=15),
                     )
        title_label.pack(pady=10)


        movie_view = self.winfo_toplevel()
        director = ""
        try:
            director = movie_view.controller.get_director(self.movie.Id)
        except Exception as e:
            print(e)

        director_label = ctk.CTkLabel(self, text=f"Reżyser: {director}", font = ctk.CTkFont(family="Roboto", size=15))
        director_label.pack(pady=10)

        rate = ctk.CTkFrame(self, fg_color="white")
        rate.pack(pady=10)
        rate_label=ctk.CTkLabel(rate, text="Ocena 1-10", font = ctk.CTkFont(family="Roboto", size=15))
        rate_label.pack(side="left", padx=10)

        self.score_field = ctk.CTkEntry(rate, width=50)
        self.score_field.pack(side="left", padx=10)

        save_button = ctk.CTkButton(self, text="Zapisz", width=50, command=self._save_rate)
        save_button.pack(pady=10)

    def _save_rate(self):
        new_score = int(self.score_field.get().strip())

        if new_score not in range(1, 11):
            return

        movie_view = self.winfo_toplevel()
        try:
            movie_view.controller.rate_movie(self.movie.Id, new_score)
        except Exception as e:
            print(e)

        try:
            self._display_image()
        except ImageLoadException as e:
            self._clear_tile()
            self._display_title(self.movie.Title)
            self._click_event()
            print(e)


    def _clear_tile(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.widgets.clear()

    def _click_event(self):
        self.bind("<Button-1>", self._handle_click)
        self.widget.bind("<Button-1>", self._handle_click)

    def _handle_click(self, event=None):
        self._display_details()
        if self.on_click:
            self.on_click(self.movie)
