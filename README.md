
# Katalog Filmów

**Autor:** Kacper Gawęda Marcin Hajduk 
**Cel:** Zarządzanie kolekcją filmów (dodawanie, przeszukiwanie, edycja) z wykorzystaniem Pythona.  
**Uruchamianie:** `python main.py`

## Przykładowe dane wejściowe (data.json)
```json
[
  {"tytul": "Matrix", "rezyser": "Wachowski", "rok": 1999, "ocena": 9.0},
  {"tytul": "Incepcja", "rezyser": "Nolan", "rok": 2010, "ocena": 8.8}
]
```

## Dane wyjściowe
Lista filmów filtrowanych, zmodyfikowanych i analizowanych przez użytkownika.

## Diagram klas

```
Film
 ├── tytul: str
 ├── rezyser: str
 ├── rok: int
 └── ocena: float
```

## Moduły:
- `main.py`: logika interakcji użytkownika (UI)
- `models.py`: definicja klasy `Film`
- `utils.py`: funkcje pomocnicze (np. zapis, sortowanie)
- `visual.py`: wykresy i wizualizacja danych
- `testy.py`: testy jednostkowe
