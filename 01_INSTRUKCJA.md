# Zadanie #1: przygotowac szkielet FastAPI i kontrakt REST

Właściciel z planu: **Bohdan Oleksiv**. Karta: https://github.com/Massage-Services-System/Massage-Services-System/issues/1

Przygotowano strukturę aplikacji, konfigurację środowiska, schematy Pydantic i wersjonowane trasy /api/v1. Dodano health-check, spójne błędy JSON, OpenAPI oraz uruchamianie przez START.cmd. Trasy funkcji biznesowych są na tym etapie jawnymi odpowiedziami 501; kolejne zadania zastępują je implementacją.

## Zależności

Zależności merytoryczne: brak — początkowy szkielet.
Paczki plików należy nakładać kolejno **#1 → #2 → … → #11**. Przed tą paczką wymagany jest stan po #0.
To pierwsza paczka — nie wymaga wcześniejszego ZIP-a.

## Dodanie do Git

Przed rozpakowaniem pobierz aktualny stan repozytorium (`git pull --ff-only`). Rozpakuj **zawartość** ZIP-a bezpośrednio do korzenia repozytorium, zachowując ścieżki. Potwierdź zastąpienie plików, które rozwija to zadanie. Następnie:

```powershell
git status --short
git add -- .gitignore .dockerignore .env.example requirements.txt requirements-preview.txt START.cmd PREVIEW_OFFLINE.cmd app/__init__.py app/config.py app/schemas.py app/preview.py app/security.py app/api.py app/main.py frontend/assets/.gitkeep frontend/index.html frontend/privacy.html README.md docs/issues/INSTRUKCJA.md docs/issues/01_COMMIT.txt docs/issues/01_INSTRUKCJA.md docs/issues/01_MANIFEST.json
git diff --cached --stat
git commit -F docs/issues/01_COMMIT.txt
git push
```

Na stronie GitHub użyj Add file → Upload files i przeciągnij rozpakowane foldery/pliki, a tytuł oraz opis skopiuj z `docs/issues/01_COMMIT.txt`. Istniejący PDF projektu pozostaje bez zmian.

## Gotowy opis

```text
feat(api): przygotowac szkielet FastAPI i kontrakt REST

Przygotowano strukturę aplikacji, konfigurację środowiska, schematy Pydantic i wersjonowane trasy /api/v1. Dodano health-check, spójne błędy JSON, OpenAPI oraz uruchamianie przez START.cmd. Trasy funkcji biznesowych są na tym etapie jawnymi odpowiedziami 501; kolejne zadania zastępują je implementacją.

Refs #1
```

## Pliki

- `.gitignore` — nowy plik
- `.dockerignore` — nowy plik
- `.env.example` — nowy plik
- `requirements.txt` — nowy plik
- `requirements-preview.txt` — nowy plik
- `START.cmd` — nowy plik
- `PREVIEW_OFFLINE.cmd` — nowy plik
- `app/__init__.py` — nowy plik
- `app/config.py` — nowy plik
- `app/schemas.py` — nowy plik
- `app/preview.py` — nowy plik
- `app/security.py` — nowy plik
- `app/api.py` — nowy plik
- `app/main.py` — nowy plik
- `frontend/assets/.gitkeep` — nowy plik
- `frontend/index.html` — nowy plik
- `frontend/privacy.html` — nowy plik
- `README.md` — nowy plik
- `docs/issues/INSTRUKCJA.md` — nowy plik
- `docs/issues/01_COMMIT.txt` — nowy plik
- `docs/issues/01_INSTRUKCJA.md` — nowy plik
- `docs/issues/01_MANIFEST.json` — nowy plik

Pliki nie są usuwane. Manifest zawiera nowe sumy SHA-256 i, przy aktualizacji, oczekiwane sumy wcześniejszej wersji. Sekrety, `.env` i baza są wykluczone. `.env.example` jest bezpiecznym wzorem, nie działającym tokenem.

Testy OpenAPI, Telegram live i browser E2E mają jawne ograniczenia opisane w dokumentacji. Paczka #11 przygotowuje wdrożenie, lecz nie tworzy publicznego hostingu.
