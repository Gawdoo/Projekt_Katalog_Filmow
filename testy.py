import unittest
import timeit
from models import Movie, Review, MovieApp

# === TESTY JEDNOSTKOWE ===
class TestMovie(unittest.TestCase):
    # Testuje inicjalizację obiektu Movie
    def test_movie_init(self):
        movie = Movie("Matrix", 1999, "Sci-Fi")
        self.assertEqual(movie.title, "Matrix")  # Sprawdza tytuł
        self.assertEqual(movie.year, 1999)  # Sprawdza rok
        self.assertEqual(movie.genre, "Sci-Fi")  # Sprawdza gatunek
        self.assertEqual(movie.reviews, [])  # Sprawdza, czy lista recenzji jest pusta

    # Testuje dodawanie recenzji i obliczanie średniej oceny
    def test_add_review_and_average(self):
        movie = Movie("Incepcja", 2010, "Sci-Fi")
        r1 = Review("Jan", 8, "Dobre")  # Tworzy pierwszą recenzję
        r2 = Review("Anna", 10, "Super")  # Tworzy drugą recenzję
        movie.add_review(r1)  # Dodaje pierwszą recenzję
        movie.add_review(r2)  # Dodaje drugą recenzję
        self.assertEqual(len(movie.reviews), 4)  # Sprawdza liczbę recenzji
        self.assertAlmostEqual(movie.average_rating(), 4.5)  # Sprawdza średnią ocenę

    # Testuje metodę __str__ obiektu Movie
    def test_str(self):
        movie = Movie("Test", 2023, "Thriller")
        self.assertIn("Test", str(movie))  # Sprawdza, czy tytuł znajduje się w opisie

# === TESTY FUNKCJONALNE ===
class TestFunctionality(unittest.TestCase):
    # Testuje przepływ dodawania filmu i recenzji w aplikacji
    def test_add_movie_and_review_flow(self):
        app = MovieApp()  # Tworzy instancję aplikacji
        initial_count = len(app.movies)  # Zapisuje początkową liczbę filmów
        movie = Movie("Testowy Film", 2022, "Dramat")  # Tworzy nowy film
        review = Review("Tester", 7, "Ok")  # Tworzy recenzję
        movie.add_review(review)  # Dodaje recenzję do filmu
        app.movies.append(movie)  # Dodaje film do aplikacji
        self.assertEqual(len(app.movies), initial_count + 1)  # Sprawdza, czy liczba filmów wzrosła
        self.assertEqual(app.movies[-1].average_rating(), 7)  # Sprawdza średnią ocenę dodanego filmu

# === TESTY INTEGRACYJNE ===
class TestIntegration(unittest.TestCase):
    # Testuje zapis i wczytywanie danych
    def test_load_and_save(self):
        app = MovieApp()  # Tworzy instancję aplikacji
        count_before = len(app.movies)  # Zapisuje początkową liczbę filmów
        # Dodaje tymczasowy film
        temp = Movie("Temp", 2000, "Test")
        app.movies.append(temp)  # Dodaje film do listy
        app.save_movies()  # Zapisuje dane do pliku

        # Wczytuje dane w nowej instancji aplikacji
        app2 = MovieApp()
        titles = [m.title for m in app2.movies]  # Pobiera tytuły filmów
        self.assertIn("Temp", titles)  # Sprawdza, czy tymczasowy film został wczytany

# === TESTY GRANICZNE ===
class TestEdgeCases(unittest.TestCase):
    # Testuje przypadek filmu bez recenzji
    def test_empty_reviews(self):
        m = Movie("Brak Recenzji", 2001, "None")
        self.assertIsNone(m.average_rating())  # Sprawdza, czy średnia jest None dla braku recenzji

    # Testuje niepoprawną ocenę w recenzji
    def test_invalid_rating(self):
        with self.assertRaises(ValueError):
            Review("Ktoś", 11, "Poza zakresem")  # Sprawdza, czy wyjątek jest zgłaszany dla oceny poza zakresem

    # Testuje dodanie nieprawidłowego typu recenzji
    def test_invalid_review_type(self):
        m = Movie("Test", 2021, "Komedia")
        with self.assertRaises(TypeError):
            m.add_review("to nie jest obiekt Review")  # Sprawdza, czy wyjątek jest zgłaszany dla nieprawidłowego typu

# === TESTY WYDAJNOŚCI ===
def test_performance():
    # Kod przygotowujący dane do testu wydajności
    setup_code = """
from utils import sortuj_po_ocenie
import json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)["movies"]
"""
    stmt = "sortuj_po_ocenie(data)"  # Testowana instrukcja
    czas = timeit.timeit(stmt, setup=setup_code, number=100, globals=globals())  # Wykonuje sortowanie 100 razy
    print(f"[PERF] Czas wykonania (100x sortowanie): {czas:.4f}s")  # Wyświetla czas wykonania

# Uruchamia testy jednostkowe i test wydajności
if __name__ == "__main__":
    unittest.main(exit=False)  # Wykonuje testy jednostkowe
    test_performance()  # Wykonuje test wydajności
