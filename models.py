import datetime
from functools import reduce

# Klasa reprezentująca recenzję filmu
class Review:
    def __init__(self, author, rating, comment):
        if not 0 <= rating <= 10:
            raise ValueError("Ocena musi być w przedziale 0-10")  # Sprawdza poprawność oceny
        self.author = author
        self.rating = rating
        self.comment = comment
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")  # Ustawia bieżącą datę

    # Zwraca tekstowy opis recenzji
    def __str__(self):
        return f"{self.author} ({self.date}) - Ocena: {self.rating}/10\nKomentarz: {self.comment}"

# Klasa reprezentująca film
class Movie:
    def __init__(self, title, year, genre):
        self.title = title
        self.year = year
        self.genre = genre
        self.reviews = []  # Lista recenzji filmu

    # Dodaje recenzję do filmu
    def add_review(self, review):
        if not isinstance(review, Review):
            raise TypeError("Dodany obiekt musi być typu Review")  # Sprawdza typ
        self.reviews.append(review)

    # Oblicza średnią ocen filmu
    def average_rating(self):
        if not self.reviews:
            return None  # Zwraca None, jeśli brak recenzji
        # Używa reduce i map do obliczenia średniej
        return round(reduce(lambda a, b: a + b, map(lambda r: r.rating, self.reviews)) / len(self.reviews), 2)

    # Zwraca tekstowy opis filmu
    def __str__(self):
        avg = self.average_rating()
        return f"{self.title} ({self.year}), Gatunek: {self.genre}, Średnia ocena: {avg if avg is not None else 'Brak ocen'}"

# Klasa zarządzająca aplikacją filmową
class MovieApp:
    def __init__(self):
        from utils import load_data
        self.data = load_data()  # Wczytuje dane z pliku JSON
        self.movies = self.load_movies()  # Tworzy obiekty Movie

    # Konwertuje dane JSON na obiekty Movie
    def load_movies(self):
        movies = []
        for m in self.data.get("movies", []):
            movie = Movie(m["title"], m["year"], m["genre"])
            for r in m.get("reviews", []):
                review = Review(r["author"], r["rating"], r["comment"])
                movie.add_review(review)
            movies.append(movie)
        return movies

    # Zapisuje filmy do pliku JSON
    def save_movies(self):
        from utils import save_data
        output = {
            "movies": [
                {
                    "title": m.title,
                    "year": m.year,
                    "genre": m.genre,
                    "reviews": [
                        {"author": r.author, "rating": r.rating, "comment": r.comment, "date": r.date}
                        for r in m.reviews
                    ],
                }
                for m in self.movies
            ]
        }
        save_data(output)

    # Uruchamia główną pętlę aplikacji
    def run(self):
        print("Witaj w katalogu filmów!")
        while True:
            # Wyświetla menu opcji
            print("\n1. Wyświetl wszystkie filmy\n2. Dodaj film\n3. Dodaj recenzję\n4. Pokaż recenzje filmu\n5. Usuń film\n6. Zobacz szczegóły filmu\n7. Zapisz i wyjdź")
            opcja = input("> ")
            if opcja == "1":
                self.list_movies_detailed()  # Wyświetla szczegóły filmów
            elif opcja == "2":
                self.add_movie()  # Dodaje nowy film
            elif opcja == "3":
                self.add_review()  # Dodaje recenzję
            elif opcja == "4":
                self.show_reviews()  # Pokazuje recenzje wybranego filmu
            elif opcja == "5":
                self.delete_movie()  # Usuwa film
            elif opcja == "6":
                self.show_movie_details()  # Pokazuje szczegóły filmu
            elif opcja == "7":
                self.save_movies()  # Zapisuje dane i kończy
                print("Zapisano dane. Do widzenia!")
                break
            else:
                print("Nieprawidłowa opcja!")

    # Dodaje nowy film na podstawie danych użytkownika
    def add_movie(self):
        title = input("Tytuł filmu: ")
        year = input("Rok produkcji: ")
        genre = input("Gatunek: ")
        try:
            movie = Movie(title, int(year), genre)
            self.movies.append(movie)
            print("Dodano film.")
        except ValueError:
            print("Nieprawidłowy rok produkcji!")

    # Dodaje recenzję do wybranego filmu
    def add_review(self):
        self.list_movies()  # Wyświetla listę filmów
        try:
            index = int(input("Wybierz numer filmu: ")) - 1
            if 0 <= index < len(self.movies):
                author = input("Autor recenzji: ")
                rating = float(input("Ocena (0-10): "))
                comment = input("Komentarz: ")
                review = Review(author, rating, comment)
                self.movies[index].add_review(review)
                print("Dodano recenzję.")
            else:
                print("Nie ma takiego filmu.")
        except Exception as e:
            print(f"Błąd: {e}")

    # Wyświetla recenzje wybranego filmu
    def show_reviews(self):
        self.list_movies()
        try:
            index = int(input("Wybierz numer filmu: ")) - 1
            if 0 <= index < len(self.movies):
                print(f"\nRecenzje filmu: {self.movies[index].title}")
                if not self.movies[index].reviews:
                    print("Brak recenzji.")
                else:
                    for r in self.movies[index].reviews:
                        print("-" * 40)
                        print(r)
            else:
                print("Nie ma takiego filmu.")
        except Exception as e:
            print(f"Błąd: {e}")

    # Usuwa wybrany film
    def delete_movie(self):
        self.list_movies()
        try:
            index = int(input("Wybierz numer filmu do usunięcia: ")) - 1
            if 0 <= index < len(self.movies):
                removed = self.movies.pop(index)
                print(f"Usunięto film: {removed.title}")
            else:
                print("Nie ma takiego filmu.")
        except Exception as e:
            print(f"Błąd: {e}")

    # Pokazuje szczegóły wybranego filmu
    def show_movie_details(self):
        self.list_movies()
        try:
            index = int(input("Wybierz numer filmu: ")) - 1
            if 0 <= index < len(self.movies):
                movie = self.movies[index]
                print("\nSzczegóły filmu:")
                print(movie)
                print("\nRecenzje:")
                if not movie.reviews:
                    print("Brak recenzji.")
                else:
                    for r in movie.reviews:
                        print("-" * 40)
                        print(r)
            else:
                print("Nie ma takiego filmu.")
        except Exception as e:
            print(f"Błąd: {e}")

    # Wyświetla listę tytułów filmów
    def list_movies(self):
        for i, movie in enumerate(self.movies):
            print(f"{i+1}. {movie.title}")

    # Wyświetla szczegółowe informacje o filmach
    def list_movies_detailed(self):
        for i, movie in enumerate(self.movies):
            print(f"{i+1}. {movie}")
