.PHONY: init dev test shell migrations migrate superuser seed check help

# Help command to list available targets
help:
	@echo "Available commands:"
	@echo "  init      - Setup environment, install dependencies, and start containers"
	@echo "  dev       - Run the Django development server"
	@echo "  check     - Run Django system checks"
	@echo "  migrate   - Apply database migrations"
	@echo "  test      - Run tests using pytest"
	@echo "  superuser - Create a Django superuser"
	@echo "  seed      - Seed the database with demo CRM data"
	@echo "  shell     - Open a Django shell"

init:
	cp -n .env.example .env || true
	pip install -r requirements.txt
	docker compose -f docker-compose.example.yml up -d db redis
	@echo "Wait for DB to be ready, then run: make migrate && make seed"

dev:
	python manage.py runserver

check:
	python manage.py check

migrate:
	python manage.py migrate

test:
	pytest

superuser:
	python manage.py createsuperuser

seed:
	python seed_crm_data.py

shell:
	python manage.py shell

migrations:
	python manage.py makemigrations
