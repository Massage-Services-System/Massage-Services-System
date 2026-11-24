# Osobna paczka dla każdego zadania #1–#11

To 11 kolejnych przyrostów jednego repozytorium. Wgrywaj **rozpakowaną zawartość** w kolejności 01 → 02 → … → 11, bez dodatkowego katalogu nadrzędnego i z zachowaniem `app/`, `frontend/`, `tests/` i `docs/`.

Pliki wspólne (np. `app/services.py` i `frontend/assets/app.js`) w późniejszych paczkach są rozwinięciem wcześniejszej wersji i należy je zastąpić. Manifest zapisuje poprzedni i nowy hash. Dlatego przed dodaniem swojego zadania pobierz aktualny stan repozytorium i nie nakładaj starego ZIP-a na nowszą wersję pliku.

Każdy ZIP ma własny opis commitu w `docs/issues/NN_COMMIT.txt` i instrukcję `NN_INSTRUKCJA.md`. Początkowe paczki zawierają jawne 501 dla funkcji planowanych w kolejnych zadaniach. Pełny kod powstaje po dodaniu wszystkich paczek.

| Zadanie | ZIP | Właściciel z planu | Zakres |
|---|---|---|---|
| #1 | `01_Issue1_FastAPI.zip` | Bohdan Oleksiv | przygotowac szkielet FastAPI i kontrakt REST |
| #2 | `02_Issue2_SQLite.zip` | Ihor Kozmuk | dodac modele SQLite SQLAlchemy i idempotentny seed |
| #3 | `03_Issue3_Telegram_Auth.zip` | Bohdan Oleksiv | weryfikowac Telegram initData i zapisywac uzytkownika |
| #4 | `04_Issue4_Catalog.zip` | Ihor Kozmuk | filtrowac katalog masazy wedlug stref ciala |
| #5 | `05_Issue5_Body_SVG.zip` | Oleksandr Zinchuk | dodac interaktywna sylwetke SVG i wybor strefy |
| #6 | `06_Issue6_Booking_API.zip` | Ihor Kozmuk; integracja Bohdan Oleksiv | sprawdzac dostepnosc i atomowo rezerwowac termin |
| #7 | `07_Issue7_Booking_Frontend.zip` | Oleksandr Zinchuk | zbudowac frontendowy proces rezerwacji |
| #8 | `08_Issue8_My_Visits.zip` | Oleksandr Zinchuk | dodac moje wizyty i potwierdzane anulowanie |
| #9 | `09_Issue9_Telegram_Integration.zip` | Bohdan Oleksiv; UI Oleksandr Zinchuk | zintegrowac WebApp z backendem i botem |
| #10 | `10_Issue10_Tests.zip` | Bohdan Oleksiv; DB Ihor; UI Oleksandr | dodac testy kontraktu auth i wspolbieznosci |
| #11 | `11_Issue11_HTTPS_Setup.zip` | Bohdan Oleksiv | przygotowac konfiguracje HTTPS i instrukcje uruchomienia |

## Git

Każdy członek zespołu klonuje to samo repozytorium. Przed rozpakowaniem pobiera poprzednie zadania przez `git pull --ff-only`. Potem rozpakowuje paczkę do korzenia i używa gotowego polecenia `git add -- ...` oraz `git commit -F docs/issues/NN_COMMIT.txt` z instrukcji swojego zadania. Może też dodać foldery przez GitHub Add file / Upload files, zachowując ścieżki.

ZIP-y są do przenoszenia plików; do Git trafiają ich rozpakowane źródła. Istniejący PDF karty projektu pozostaje na miejscu. Paczki nie usuwają plików i nie zawierają tokenu, `.env`, bazy, `.git`, `.venv` ani cache.

## Stan weryfikacji

Końcowy kod ma 44 zaliczone testy i 1 pominięty test OpenAPI w środowisku bez FastAPI. Telegram live i browser E2E nie są jeszcze potwierdzone. Paczka #11 to przygotowanie konfiguracji i instrukcji, a nie wykonane publiczne wdrożenie HTTPS. Opisy używają `Refs`, nie `Closes`.
