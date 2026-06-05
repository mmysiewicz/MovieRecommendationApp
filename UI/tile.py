import os
import customtkinter as ctk
from Exceptions.Exceptions import ImageLoadException
from PIL import Image


class Tile(ctk.CTkFrame):
    def __init__(self, master, movie, on_click):
        super().__init__(master, width=100, height=300, cursor="hand2",
                         fg_color=("#EAEAEA", "#2B2B2B"))
        self.movie = movie
        self.on_click = on_click

        self.grid_propagate(False)
        self.pack_propagate(False)

        try:
            self._render_image()
        except ImageLoadException as e:
            print(e)

        self._click_event()


    def _render_image(self):

        if self.movie.poster_path is not None and os.path.exists(self.movie.poster_path):
            try:
                image = Image.open(self.movie.poster_path)
                ctkinter = ctk.CTkImage(light_image=image, dark_image=image, size=(200, 300))

                self.widget = ctk.CTkLabel(self, image=ctkinter, text="")
                self.widget.pack(pady=10, padx=10)


            except Exception as e:
                self._render_text(self.movie.Title)
                raise ImageLoadException(
                   "Plik ma niepoprawny format lub jest uszkodzony",
                   self.movie.Title,
                   self.movie.poster_path)

        else:
            self._render_text(self.movie.Title)
            raise ImageLoadException(
                "Plik nie istnieje",
                self.movie.Title,
                self.movie.poster_path)

    def _render_text(self, text):
        self.widget = ctk.CTkLabel(self, text=text, font = ctk.CTkFont(family="Roboto", size=20))
        self.widget.pack(pady=100, padx=10, fill="both", expand=True)

    def _click_event(self):
        self.bind("<Button-1>", self._handle_click)
        self.widget.bind("<Button-1>", self._handle_click)

    def _handle_click(self, event=None):
        if self.on_click:
            self.on_click(self.movie)
