# Zadanie #5: dodac interaktywna sylwetke SVG i wybor strefy

Właściciel z planu: **Oleksandr Zinchuk**. Karta: https://github.com/Massage-Services-System/Massage-Services-System/issues/5

Dodano czarno-złoty, responsywny układ z lotosem, mapą SVG i katalogiem. Strefy mają hover, selected, nazwy dostępności, obsługę Enter/Spacja i listę alternatywną. Wybór strefy pobiera pasujące masaże z API. Wspólny układ zawiera miejsca na późniejsze kroki rezerwacji; ich logika dochodzi w #7 i #8, a integracja klienta Telegram w #9.

## Zależności

Zależności merytoryczne: #1, #4.
Paczki plików należy nakładać kolejno **#1 → #2 → … → #11**. Przed tą paczką wymagany jest stan po #4.
Wspólne pliki zastępują wcześniejszą wersję z tego samego repozytorium. Nie usuwaj całych folderów.

## Dodanie do Git

Przed rozpakowaniem pobierz aktualny stan repozytorium (`git pull --ff-only`). Rozpakuj **zawartość** ZIP-a bezpośrednio do korzenia repozytorium, zachowując ścieżki. Potwierdź zastąpienie plików, które rozwija to zadanie. Następnie:

```powershell
git status --short
git add -- frontend/privacy.html frontend/assets/style.css frontend/assets/readability.css frontend/assets/lotus.png frontend/index.html frontend/assets/app.js docs/issues/05_COMMIT.txt docs/issues/05_INSTRUKCJA.md docs/issues/05_MANIFEST.json
git diff --cached --stat
git commit -F docs/issues/05_COMMIT.txt
git push
```

Na stronie GitHub użyj Add file → Upload files i przeciągnij rozpakowane foldery/pliki, a tytuł oraz opis skopiuj z `docs/issues/05_COMMIT.txt`. Istniejący PDF projektu pozostaje bez zmian.

## Gotowy opis

```text
feat(ui): dodac interaktywna sylwetke SVG i wybor strefy

Dodano czarno-złoty, responsywny układ z lotosem, mapą SVG i katalogiem. Strefy mają hover, selected, nazwy dostępności, obsługę Enter/Spacja i listę alternatywną. Wybór strefy pobiera pasujące masaże z API. Wspólny układ zawiera miejsca na późniejsze kroki rezerwacji; ich logika dochodzi w #7 i #8, a integracja klienta Telegram w #9.

Refs #5
```

## Pliki

- `frontend/privacy.html` — aktualizacja
- `frontend/assets/style.css` — nowy plik
- `frontend/assets/readability.css` — nowy plik
- `frontend/assets/lotus.png` — nowy plik
- `frontend/index.html` — aktualizacja
- `frontend/assets/app.js` — nowy plik
- `docs/issues/05_COMMIT.txt` — nowy plik
- `docs/issues/05_INSTRUKCJA.md` — nowy plik
- `docs/issues/05_MANIFEST.json` — nowy plik

Pliki nie są usuwane. Manifest zawiera nowe sumy SHA-256 i, przy aktualizacji, oczekiwane sumy wcześniejszej wersji. Sekrety, `.env` i baza są wykluczone. `.env.example` jest bezpiecznym wzorem, nie działającym tokenem.

Testy OpenAPI, Telegram live i browser E2E mają jawne ograniczenia opisane w dokumentacji. Paczka #11 przygotowuje wdrożenie, lecz nie tworzy publicznego hostingu.
