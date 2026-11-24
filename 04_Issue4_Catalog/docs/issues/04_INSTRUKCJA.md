# Zadanie #4: filtrowac katalog masazy wedlug stref ciala

Właściciel z planu: **Ihor Kozmuk**. Karta: https://github.com/Massage-Services-System/Massage-Services-System/issues/4

Udostępniono strefy ciała, katalog masaży i listę masażystów przez API. Filtrowanie korzysta z relacji SQLAlchemy; odpowiedzi zawierają opis, czas, cenę i przypisane strefy. Pusty lub nieznany filtr zwraca 422. Seed jest demonstracyjny i wymaga porównania z PDF karty projektu.

## Zależności

Zależności merytoryczne: #2, #3.
Paczki plików należy nakładać kolejno **#1 → #2 → … → #11**. Przed tą paczką wymagany jest stan po #3.
Wspólne pliki zastępują wcześniejszą wersję z tego samego repozytorium. Nie usuwaj całych folderów.

## Dodanie do Git

Przed rozpakowaniem pobierz aktualny stan repozytorium (`git pull --ff-only`). Rozpakuj **zawartość** ZIP-a bezpośrednio do korzenia repozytorium, zachowując ścieżki. Potwierdź zastąpienie plików, które rozwija to zadanie. Następnie:

```powershell
git status --short
git add -- app/services.py docs/issues/04_COMMIT.txt docs/issues/04_INSTRUKCJA.md docs/issues/04_MANIFEST.json
git diff --cached --stat
git commit -F docs/issues/04_COMMIT.txt
git push
```

Na stronie GitHub użyj Add file → Upload files i przeciągnij rozpakowane foldery/pliki, a tytuł oraz opis skopiuj z `docs/issues/04_COMMIT.txt`. Istniejący PDF projektu pozostaje bez zmian.

## Gotowy opis

```text
feat(catalog): filtrowac katalog masazy wedlug stref ciala

Udostępniono strefy ciała, katalog masaży i listę masażystów przez API. Filtrowanie korzysta z relacji SQLAlchemy; odpowiedzi zawierają opis, czas, cenę i przypisane strefy. Pusty lub nieznany filtr zwraca 422. Seed jest demonstracyjny i wymaga porównania z PDF karty projektu.

Refs #4
```

## Pliki

- `app/services.py` — aktualizacja
- `docs/issues/04_COMMIT.txt` — nowy plik
- `docs/issues/04_INSTRUKCJA.md` — nowy plik
- `docs/issues/04_MANIFEST.json` — nowy plik

Pliki nie są usuwane. Manifest zawiera nowe sumy SHA-256 i, przy aktualizacji, oczekiwane sumy wcześniejszej wersji. Sekrety, `.env` i baza są wykluczone. `.env.example` jest bezpiecznym wzorem, nie działającym tokenem.

Testy OpenAPI, Telegram live i browser E2E mają jawne ograniczenia opisane w dokumentacji. Paczka #11 przygotowuje wdrożenie, lecz nie tworzy publicznego hostingu.
