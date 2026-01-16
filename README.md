# VAII Doprava

## Inštalácia
- Python 3.13, MySQL
- `py -m venv .venv && .venv\Scripts\activate`
- `pip install -r requirements.txt` (alebo `pip install django mysqlclient`)
- Nastav DB v doprava/settings.py (DATABASES)
- `py manage.py migrate`
- `py manage.py createsuperuser`
- (voliteľné) `py manage.py collectstatic`

## Spustenie
- `py manage.py runserver`
- http://127.0.0.1:8000/

## Funkcie
- Prihlásenie/registrácia, profil + edit
- Roly: admin vs registrovaný, ochrana admin-only CRUD
- Správa používateľov: filter, paginácia (AJAX), udelenie/odobratie admin práv (AJAX)
- Reset hesla emailom (console backend)
- Správa trás/vozidiel/zastávok (CRUD)

## Poznámky k bezpečnosti
- CSRF zapnuté, validácie vo formulároch
- Debug vypnúť v produkcii, nastaviť ALLOWED_HOSTS