import matplotlib.pyplot as plt
import json
import os

# Funkcja generuje wykres słupkowy średnich ocen filmów
def wykres_ocen(json_file, output_file="oceny.png"):
    # Wczytuje dane z pliku JSON
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)["movies"]

    tytuly = []  # Lista tytułów filmów
    oceny = []  # Lista średnich ocen
    for film in data:
        reviews = film.get("reviews", [])  # Pobiera recenzje filmu
        if reviews:
            # Oblicza średnią ocenę filmu
            avg = sum([r["rating"] for r in reviews]) / len(reviews)
            tytuly.append(film["title"])  # Dodaje tytuł do listy
            oceny.append(avg)  # Dodaje średnią ocenę do listy

    # Sprawdza, czy są dane do wykresu
    if not tytuly:
        print("Brak danych do wygenerowania wykresu.")
        return

    # Tworzy wykres słupkowy
    plt.figure(figsize=(10, 6))  # Ustawia rozmiar wykresu
    plt.bar(tytuly, oceny, color='skyblue')  # Tworzy słupki
    plt.title("Średnie oceny filmów")  # Ustawia tytuł wykresu
    plt.xlabel("Tytuł")  # Ustawia etykietę osi X
    plt.ylabel("Średnia ocena")  # Ustawia etykietę osi Y
    plt.xticks(rotation=45)  # Obraca etykiety osi X dla czytelności
    plt.tight_layout()  # Dopasowuje układ wykresu
    plt.savefig(output_file)  # Zapisuje wykres do pliku
    plt.close()  # Zamyka wykres, aby zwolnić pamięć

    # Pobiera pełną ścieżkę do pliku wykresu
    full_path = os.path.abspath(output_file)
    print(f"Wykres zapisano jako: {full_path}")
    try:
        os.startfile(full_path)  # Próbuje automatycznie otworzyć plik (tylko Windows)
    except Exception as e:
        print("Nie udało się otworzyć wykresu automatycznie:", e)  # Obsługuje błąd otwarcia
