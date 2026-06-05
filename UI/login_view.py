import customtkinter as ctk
from Controllers.user_controller import UserController


class LoginView(ctk.CTk):
    def __init__(self, user_controller : UserController, on_login_succeed):
        super().__init__()
        self.user_controller = user_controller
        self.on_login_succeed = on_login_succeed

        self.protocol("WM_DELETE_WINDOW", self._handle_close)
        self.title("Movie recommender")
        self.geometry("400x300")
        self.resizable(True, True)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.label = ctk.CTkLabel(self, text="Wprowadź dane", font=ctk.CTkFont(family="Roboto", size=20, weight="bold"))
        self.label.pack(pady=20)

        self.login_field = ctk.CTkEntry(self, width=200, placeholder_text="Login")
        self.login_field.pack(pady=10)

        self.password_field = ctk.CTkEntry(self, width=200, placeholder_text="Hasło", show="*")
        self.password_field.pack(pady=10)

        self.error_info = ctk.CTkLabel(self, text="", text_color="red",  font=ctk.CTkFont(family="Roboto", size=15, weight="bold"))
        self.error_info.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Zaloguj się", width=200, command=self._handle_button)
        self.login_button.pack(pady=10)

    def _handle_button(self):
        login = self.login_field.get()
        password = self.password_field.get()

        if not login or not password:
            self.error_info.configure(text="Pola nie mogą być puste")
            return

        user = self.user_controller.login(login, password)

        if user:
            self.withdraw()
            self.on_login_succeed(user)
        else:
            self.error_info.configure(text="Niepoprawne dane")

    def _handle_close(self):
        self.destroy()
