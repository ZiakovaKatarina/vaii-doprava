import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doprava.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
    
    cursor.execute("DROP TABLE IF EXISTS data_management_routestop")
    cursor.execute("DROP TABLE IF EXISTS data_management_trip")
    cursor.execute("DROP TABLE IF EXISTS data_management_route")
    cursor.execute("DROP TABLE IF EXISTS data_management_stop")
    cursor.execute("DROP TABLE IF EXISTS data_management_vehicle")
    
    cursor.execute("DELETE FROM django_migrations WHERE app='data_management'")
    
    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
    
    print("✅ Tabuľky a migrácie vymazané")