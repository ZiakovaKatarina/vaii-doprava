# VAII Doprava - Verejná Doprava

Webová aplikácia pre správu verejnej dopravy s AJAX filtovaním, prihlasovaním a rôznymi rolami.

## Požiadavky
- Python 3.13+
- MySQL/MariaDB 10.4+
- pip

## Inštalácia

### 1. Klonovanie projektu
```bash
git clone https://github.com/USERNAME/vaii-doprava.git
cd vaii-doprava
```

### 2. Inštalácia závislosti
```bash
pip install -r requirements.txt
```

Alebo ručne:
```bash
pip install django==4.2.27 mysqlclient pymysql
```

### 3. Nastavenie databázu
Vytvorenie databázy:
```sql
CREATE DATABASE doprava_db CHARACTER SET utf8mb4;
```

Upravenie `doprava/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'doprava_db',
        'USER': 'root',
        'PASSWORD': 'vaše_heslo',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. Migrácie a superuser
```bash
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
```

### 5. Spustenie serveru
```bash
py manage.py runserver
```
Otvorte http://127.0.0.1:8000/

## Bezpečnosť
- CSRF ochrana (`{% csrf_token %}` na všetkých POST)
- Validácia na serveri + klientovi
- Autentifikácia + autorizácia (`login_required`, `admin_required`)
- SQL Injection ochrana (Django ORM)
- Password hashing (Django default)

## AJAX Volania
1. **Editovanie v tabuľke** - `frontend/static/js/inline-edit.js`
   - Dvojklik na bunku → PATCH request

2. **Admin práva používateľov** - `frontend/static/js/users.js`
   - Toggle checkbox → POST request

3. **Filtrovanie + Paginácia** - `frontend/static/js/users.js`
   - Hľadanie → GET request (200+ riadkov kódu)

## Roly
Rola            Práva
Admin           všetky CRUD, správa používateľov
Registrovaný    Čítanie, obľúbené trasy
Anonymný        Iba čítanie verejných dát

## 📁 Štruktúra

```
vaii-doprava/
├── users/              # Auth, registrácia, roly
├── data_management/    # CRUD: Stop, Route, Trip, Vehicle
├── frontend/           # Verejná časť + AJAX scripty
├── personalization/    # Obľúbené trasy
├── doprava/            # Settings, URLs
├── README.md
├── requirements.txt
└── manage.py
```

## 📝 Autori

Katarína Žiaková - Semestrálna práca VAII 2025