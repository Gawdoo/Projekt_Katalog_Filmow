from functools import reduce
import time
import json

# Dekorator mierzący czas wykonania funkcji
def loguj(funkcja):
    def wrapper(*args, **kwargs):
        start = time.time()  # Zapisuje czas rozpoczęcia
        wynik = funkcja(*args, **kwargs)  # Wykonuje funkcję
        # Wyświetla czas wykonania
        print(f"[LOG] Funkcja '{funkcja.__name__}' wykonana w {time.time() - start:.4f}s")
        return wynik
    return wrapper

# Sortuje filmy po średniej ocenie (z użyciem dekoratora loguj)
@loguj
def sortuj_po_ocenie(filmy):
    # Oblicza średnią ocen dla filmu
    def srednia(f):
        oceny = [r["rating"] for r in f["reviews"]]
        return sum(oceny) / len(oceny) if oceny else 0
    return sorted(filmy, key=srednia, reverse=True)  # Sortuje malejąco

# Oblicza średnią ocen wszystkich filmów rekurencyjnie
def srednia_ocen_rekurencyjna(filmy, n=None):
    if n is None:
        n = len(filmy)  # Ustawia n na liczbę filmów, jeśli nie podano
    if n == 0:
        return 0  # Zwraca 0 dla pustej listy
    f = filmy[n - 1]  # Pobiera ostatni film
    oceny = [r["rating"] for r in f["reviews"]]  # Pobiera oceny
    sr = sum(oceny) / len(oceny) if oceny else 0  # Oblicza średnią dla filmu
    # Rekurencyjnie oblicza średnią dla reszty
    return (sr + (n - 1) * srednia_ocen_rekurencyjna(filmy, n - 1)) / n

# Filtruje filmy na podstawie minimalnej średniej oceny
def przefiltruj_filmy(filmy, prog=8.0):
    return list(filter(
        # Sprawdza, czy średnia ocen filmu jest większa lub równa progowi
        lambda f: sum([r["rating"] for r in f["reviews"]]) / len(f["reviews"]) >= prog if f["reviews"] else False,
        filmy
    ))

# Wczytuje dane z pliku JSON
def load_data(filename="data.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# Zapisuje dane do pliku JSON
def save_data(data, filename="data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
