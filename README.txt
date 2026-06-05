Aplikacja desktopowa służąca do przeglądania bazy filmów, oceniania ich oraz otrzymywania rekomendacji.

Fukcjonalności:
System logowania
Przeglądanie bazy za pomocą interfejsu z kafelkami, obsługującymi pliki .jpg
System ocen w skali 1-10
Algorytm rekomendacji oparty na ocenach wystawionych przez użytkownika. Rekomendacje generowane są poprzez obliczenie prawdopodobieństwa cosinusowego.
Eksport ocen użytkowników do pliku .json, automatyczny po wyłączeniu aplikacji.

Architektura:
Projekt został stworzony w oparciu o wzorzec MVC:
Models: Definicje tabel przy pomocy biblioteki SQLAlchemy
Repositories: Warstwa dostępu do danych
Services: Logika biznesowa
Controllers: Wartstwa pośrednicząca między UI a logiką biznesową
UI: Interfejs stworzony przy użyciu biblioteki CustomTkinter

Wymagania techniczne:
SQL Server (sterownik ODBC Driver 18)
Biblioteki: sqlalchemy, pyodbc, customtkinter, pillow

Instrukcja uruchomienia
Opcja 1:
W głównym folderze projektu wykonaj:
python -m venv venv
venv\Scripts\activate
pip install sqlalchemy pyodbc customtkinter pillow
python main.py

Opcja 2:
Uruchom przy pomocy stosownego IDE.

