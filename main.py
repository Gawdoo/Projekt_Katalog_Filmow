import json
from utils import srednia_ocen_rekurencyjna, przefiltruj_filmy, sortuj_po_ocenie
from visual import wykres_ocen

# Funkcja wczytuje dane o filmach z pliku JSON
def wczytaj_dane(plik="data.json"):
    with open(plik, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["movies"]  # Zwraca listę filmów

# Funkcja zapisuje dane filmów do pliku JSON
def zapisz_dane(filmy, plik="data.json"):
    with open(plik, "w", encoding="utf-8") as f:
        json.dump({"movies": filmy}, f, ensure_ascii=False, indent=2)  # Zapisuje dane z wcięciami

# Wyświetla menu opcji dla użytkownika
def menu():
    print("\n1. Wyświetl filmy")
    print("2. Dodaj film")
    print("3. Sortuj po średniej ocenie")
    print("4. Średnia ocen (rekurencyjnie)")
    print("5. Filtruj filmy")
    print("6. Wykres ocen")
    print("0. Wyjście")

# Wyświetla listę filmów z ich średnią oceną
def wyswietl(filmy):
    for f in filmy:
        oceny = [r["rating"] for r in f["reviews"]]  # Pobiera oceny z recenzji
        srednia = sum(oceny) / len(oceny) if oceny else 0  # Oblicza średnią, jeśli są oceny
        print(f"{f['title']} ({f['year']}) - {f['genre']} | Śr. ocena: {srednia:.2f}")  # Wyświetla dane filmu

# Dodaje nowy film do listy na podstawie danych od użytkownika
def dodaj_film(filmy):
    title = input("Tytuł: ")
    year = int(input("Rok: "))
    genre = input("Gatunek: ")
    rating = float(input("Ocena (np. 8.5): ").replace(",", "."))  # Zamienia przecinek na kropkę
    author = input("Autor oceny: ")
    comment = input("Komentarz: ")

    # Tworzy słownik reprezentujący film z jedną recenzją
    film = {
        "title": title,
        "year": year,
        "genre": genre,
        "reviews": [{
            "author": author,
            "rating": rating,
            "comment": comment,
            "date": "2025-06-22"  # Stała data dla recenzji
        }]
    }
    filmy.append(film)  # Dodaje film do listy
    print("Dodano film.")

# Główna pętla programu
if __name__ == "__main__":
    filmy = wczytaj_dane()  # Wczytuje dane na start
    while True:
        menu()  # Wyświetla menu
        wybor = input("Wybierz opcję: ")  # Pobiera wybór użytkownika
        if wybor == "1":
            wyswietl(filmy)  # Wyświetla filmy
        elif wybor == "2":
            dodaj_film(filmy)  # Dodaje nowy film
            zapisz_dane(filmy)  # Zapisuje zmiany
        elif wybor == "3":
            wynik = sortuj_po_ocenie(filmy)  # Sortuje filmy po ocenie
            wyswietl(wynik)  # Wyświetla posortowane filmy
        elif wybor == "4":
            # Oblicza średnią ocen wszystkich filmów rekurencyjnie
            print(f"Średnia wszystkich ocen: {srednia_ocen_rekurencyjna(filmy):.2f}")
        elif wybor == "5":
            # Filtruje filmy na podstawie minimalnej średniej oceny
            prog = float(input("Podaj minimalną średnią ocenę (np. 7.5): ").replace(",", "."))
            wynik = przefiltruj_filmy(filmy, prog=prog)
            wyswietl(wynik)  # Wyświetla przefiltrowane filmy
        elif wybor == "6":
            wykres_ocen("data.json")  # Generuje wykres ocen
        elif wybor == "0":
            break  # Kończy program
        else:
            print("Nieprawidłowy wybór.")  # Obsługuje błędny wybór
