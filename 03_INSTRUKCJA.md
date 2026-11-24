# Zadanie #3: weryfikowac Telegram initData i zapisywac uzytkownika

Właściciel z planu: **Bohdan Oleksiv**. Karta: https://github.com/Massage-Services-System/Massage-Services-System/issues/3

Zaimplementowano weryfikację HMAC-SHA256 Telegram initData, kontrolę czasu i podpisane sesje. Użytkownik jest tworzony lub aktualizowany idempotentnie. Nieprawidłowe dane zwracają jawne błędy 4xx. Lokalny tryb demo jest ograniczony do loopback i wyłączany w produkcji. Katalog i rezerwacje zostaną dodane w kolejnych zadaniach.

## Zależności

Zależności merytoryczne: #1, #2.
Paczki plików należy nakładać kolejno **#1 → #2 → … → #11**. Przed tą paczką wymagany jest stan po #2.
Wspólne pliki zastępują wcześniejszą wersję z tego samego repozytorium. Nie usuwaj całych folderów.

## Dodanie do Git

Przed rozpakowaniem pobierz aktualny stan repozytorium (`git pull --ff-only`). Rozpakuj **zawartość** ZIP-a bezpośrednio do korzenia repozytorium, zachowując ścieżki. Potwierdź zastąpienie plików, które rozwija to zadanie. Następnie:

```powershell
git status --short
git add -- app/security.py app/api.py app/services.py docs/issues/03_COMMIT.txt docs/issues/03_INSTRUKCJA.md docs/issues/03_MANIFEST.json
git diff --cached --stat
git commit -F docs/issues/03_COMMIT.txt
git push
```

Na stronie GitHub użyj Add file → Upload files i przeciągnij rozpakowane foldery/pliki, a tytuł oraz opis skopiuj z `docs/issues/03_COMMIT.txt`. Istniejący PDF projektu pozostaje bez zmian.

## Gotowy opis

```text
feat(auth): weryfikowac Telegram initData i zapisywac uzytkownika

Zaimplementowano weryfikację HMAC-SHA256 Telegram initData, kontrolę czasu i podpisane sesje. Użytkownik jest tworzony lub aktualizowany idempotentnie. Nieprawidłowe dane zwracają jawne błędy 4xx. Lokalny tryb demo jest ograniczony do loopback i wyłączany w produkcji. Katalog i rezerwacje zostaną dodane w kolejnych zadaniach.

Refs #3
```

## Pliki

- `app/security.py` — aktualizacja
- `app/api.py` — aktualizacja
- `app/services.py` — nowy plik
- `docs/issues/03_COMMIT.txt` — nowy plik
- `docs/issues/03_INSTRUKCJA.md` — nowy plik
- `docs/issues/03_MANIFEST.json` — nowy plik

Pliki nie są usuwane. Manifest zawiera nowe sumy SHA-256 i, przy aktualizacji, oczekiwane sumy wcześniejszej wersji. Sekrety, `.env` i baza są wykluczone. `.env.example` jest bezpiecznym wzorem, nie działającym tokenem.

Testy OpenAPI, Telegram live i browser E2E mają jawne ograniczenia opisane w dokumentacji. Paczka #11 przygotowuje wdrożenie, lecz nie tworzy publicznego hostingu.
