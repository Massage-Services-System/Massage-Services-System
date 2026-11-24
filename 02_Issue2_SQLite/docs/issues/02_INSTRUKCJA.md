# Zadanie #2: dodac modele SQLite SQLAlchemy i idempotentny seed

Właściciel z planu: **Ihor Kozmuk**. Karta: https://github.com/Massage-Services-System/Massage-Services-System/issues/2

Dodano modele użytkowników, masażystów, grafików, masaży, stref ciała i rezerwacji. Inicjalizacja tworzy tabele i idempotentnie ładuje dane demonstracyjne. Relacje katalogu i złożony klucz zajętych slotów przygotowują bazę do sprawdzania dostępności. Konkretne dane z PDF wymagają jeszcze porównania z kartą projektu.

## Zależności

Zależności merytoryczne: #1.
Paczki plików należy nakładać kolejno **#1 → #2 → … → #11**. Przed tą paczką wymagany jest stan po #1.
Wspólne pliki zastępują wcześniejszą wersję z tego samego repozytorium. Nie usuwaj całych folderów.

## Dodanie do Git

Przed rozpakowaniem pobierz aktualny stan repozytorium (`git pull --ff-only`). Rozpakuj **zawartość** ZIP-a bezpośrednio do korzenia repozytorium, zachowując ścieżki. Potwierdź zastąpienie plików, które rozwija to zadanie. Następnie:

```powershell
git status --short
git add -- app/models.py app/seed.py app/api.py docs/issues/02_COMMIT.txt docs/issues/02_INSTRUKCJA.md docs/issues/02_MANIFEST.json
git diff --cached --stat
git commit -F docs/issues/02_COMMIT.txt
git push
```

Na stronie GitHub użyj Add file → Upload files i przeciągnij rozpakowane foldery/pliki, a tytuł oraz opis skopiuj z `docs/issues/02_COMMIT.txt`. Istniejący PDF projektu pozostaje bez zmian.

## Gotowy opis

```text
feat(db): dodac modele SQLite SQLAlchemy i idempotentny seed

Dodano modele użytkowników, masażystów, grafików, masaży, stref ciała i rezerwacji. Inicjalizacja tworzy tabele i idempotentnie ładuje dane demonstracyjne. Relacje katalogu i złożony klucz zajętych slotów przygotowują bazę do sprawdzania dostępności. Konkretne dane z PDF wymagają jeszcze porównania z kartą projektu.

Refs #2
```

## Pliki

- `app/models.py` — nowy plik
- `app/seed.py` — nowy plik
- `app/api.py` — aktualizacja
- `docs/issues/02_COMMIT.txt` — nowy plik
- `docs/issues/02_INSTRUKCJA.md` — nowy plik
- `docs/issues/02_MANIFEST.json` — nowy plik

Pliki nie są usuwane. Manifest zawiera nowe sumy SHA-256 i, przy aktualizacji, oczekiwane sumy wcześniejszej wersji. Sekrety, `.env` i baza są wykluczone. `.env.example` jest bezpiecznym wzorem, nie działającym tokenem.

Testy OpenAPI, Telegram live i browser E2E mają jawne ograniczenia opisane w dokumentacji. Paczka #11 przygotowuje wdrożenie, lecz nie tworzy publicznego hostingu.
