# Systém pre správu verejnej dopravy

Tento projekt je semestrálna práca z predmetu **Vývoj aplikácií pre internet a intranet** na Žilinskej univerzite v Žiline. Ide o komplexnú webovú aplikáciu postavenú na frameworku **Django**, ktorá slúži na správu zastávok, liniek a spojov s pokročilým vyhľadávaním a interaktívnou mapovou vizualizáciou.

## Autor
- **Meno a priezvisko:** Katarína Žiaková
- **Študijná skupina:** 5ZYI31
- **Akademický rok:** 2025/2026
- **Predmet:** Vývoj aplikácií pre internet a intranet (VAII)

## Kľúčové funkcionality
- **Kompletný CRUD:** Správa zastávok, dopravných vozidiel, liniek (trás) a konkrétnych spojov.
- **Interaktívna mapa (Leaflet.js):**
    - Výber súradníc novej zastávky priamo kliknutím do mapy.
    - Integrovaný Geocoding pre hľadanie reálnych adries.
    - Vizualizácia siete zastávok a rýchle nastavenie Štartu/Cieľa kliknutím na marker.
- **Pokročilé vyhľadávanie spojení:**
    - Algoritmus vyhľadáva priame spoje medzi zastávkami.
    - V prípade neexistencie priameho spoja systém automaticky navrhne **prestup** na spoločnej zastávke dvoch rôznych liniek.
- **Personalizácia:** Možnosť registrácie používateľa a ukladania vyhľadaných trás do zoznamu obľúbených.
- **Dátový import:** Hromadné nahrávanie a aktualizácia zastávok zo súboru **CSV**.
- **Administrácia používateľov:** Dynamická AJAX tabuľka s pokročilým filtrovaním, radením, pagináciou a správou oprávnení.

## Technické požiadavky
- **Python:** 3.13+
- **Databáza:** MySQL / MariaDB 10.4+
- **Knižnice:** Django 4.2.27, mysqlclient, PyMySQL, Leaflet.js

## Inštalácia a spustenie

### 1. Príprava databázy
Vytvorte prázdnu databázu v MySQL (napr. cez phpMyAdmin alebo terminál):
```sql
CREATE DATABASE doprava_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Klonovanie a inštalácia závislostí
```Bash
git clone https://github.com/vash-repo/vaii-doprava.git
cd vaii-doprava
pip install -r requirements.txt
```

### 3. Konfigurácia
V súbore doprava/settings.py upravte sekciu DATABASES (meno používateľa a heslo), aby zodpovedala vašej lokálnej konfigurácii MySQL.
### 4. Migrácie a vytvorenie administrátora
```Bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Spustenie servera
```Bash
python manage.py runserver
```
Aplikácia bude dostupná na adrese: http://127.0.0.1:8000/

## Vyhlásenie o použití AI
V súlade s podmienkami semestrálnej práce vyhlasujem, že pri návrhu niektorých častí kódu boli použité nástroje generatívnej umelej inteligencie (ChatGPT):

- Vyhľadávací algoritmus: Návrh logiky pre hľadanie prestupných bodov.
- Integrácia mapy: Pomoc s JavaScriptovou logikou.
- Validácia: Pomoc s JavaScriptovou logikou pre prácu s validáciou na strane servera a na strane klienta.

Poznámka: Všetky AI vygenerované časti boli následne autorom manuálne upravené, integrované do architektúry projektu a riadne otestované.

---
2025 – Katarína Žiaková – VAII UNIZA