# Zadanie #7: zbudowac frontendowy proces rezerwacji

Właściciel z planu: **Oleksandr Zinchuk**. Karta: https://github.com/Massage-Services-System/Massage-Services-System/issues/7

Uruchomiono proces masaż–masażysta–data–wolna godzina–podsumowanie–potwierdzenie z identyfikatorem wizyty. Frontend pobiera dostępność z rzeczywistego API, chroni przed wielokrotnym wysłaniem i zachowuje kontekst po konflikcie 409. Na tym etapie przegląd działa przez lokalne konto demo; logowanie w kliencie Telegram dołącza #9.

## Zależności

Zależności merytoryczne: #3, #5, #6.
Paczki plików należy nakładać kolejno **#1 → #2 → … → #11**. Przed tą paczką wymagany jest stan po #6.
Wspólne pliki zastępują wcześniejszą wersję z tego samego repozytorium. Nie usuwaj całych folderów.

## Dodanie do Git

Przed rozpakowaniem pobierz aktualny stan repozytorium (`git pull --ff-only`). Rozpakuj **zawartość** ZIP-a bezpośrednio do korzenia repozytorium, zachowując ścieżki. Potwierdź zastąpienie plików, które rozwija to zadanie. Następnie:

```powershell
git status --short
git add -- frontend/assets/app.js docs/issues/07_COMMIT.txt docs/issues/07_INSTRUKCJA.md docs/issues/07_MANIFEST.json
git diff --cached --stat
git commit -F docs/issues/07_COMMIT.txt
git push
```

Na stronie GitHub użyj Add file → Upload files i przeciągnij rozpakowane foldery/pliki, a tytuł oraz opis skopiuj z `docs/issues/07_COMMIT.txt`. Istniejący PDF projektu pozostaje bez zmian.

## Gotowy opis

```text
feat(ui): zbudowac frontendowy proces rezerwacji

Uruchomiono proces masaż–masażysta–data–wolna godzina–podsumowanie–potwierdzenie z identyfikatorem wizyty. Frontend pobiera dostępność z rzeczywistego API, chroni przed wielokrotnym wysłaniem i zachowuje kontekst po konflikcie 409. Na tym etapie przegląd działa przez lokalne konto demo; logowanie w kliencie Telegram dołącza #9.

Refs #7
```

## Pliki

- `frontend/assets/app.js` — aktualizacja
- `docs/issues/07_COMMIT.txt` — nowy plik
- `docs/issues/07_INSTRUKCJA.md` — nowy plik
- `docs/issues/07_MANIFEST.json` — nowy plik

Pliki nie są usuwane. Manifest zawiera nowe sumy SHA-256 i, przy aktualizacji, oczekiwane sumy wcześniejszej wersji. Sekrety, `.env` i baza są wykluczone. `.env.example` jest bezpiecznym wzorem, nie działającym tokenem.

Testy OpenAPI, Telegram live i browser E2E mają jawne ograniczenia opisane w dokumentacji. Paczka #11 przygotowuje wdrożenie, lecz nie tworzy publicznego hostingu.
