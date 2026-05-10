import os
import sys

crm_path = os.path.abspath('templates_library/agency-crm')
sys.path.insert(0, crm_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['DEBUG'] = 'True'
os.environ['SECRET_KEY'] = 'fake-key'
os.environ['DATABASE_URL'] = 'sqlite:///db.sqlite3'

import django
django.setup()

from django.core.management import call_command

print("Running system checks...")
try:
    call_command('check')
    print("Checks passed!")
except Exception as e:
    print(f"Checks failed: {e}")

print("\nRunning migrations to test schema...")
try:
    call_command('migrate')
    print("Migrations passed!")
except Exception as e:
    print(f"Migrations failed: {e}")
