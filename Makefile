# Note: This Makefile uses "docker-compose" syntax. Users with Docker Compose v2 may replace it with "docker compose" if needed.

# Makefile for Django SaaS Template Marketplace

.PHONY: init dev check migrate makemigrations migration-check verify test shell superuser logs celery down

init:
	docker-compose up --build -d
	docker-compose exec web python manage.py migrate

dev:
	docker-compose up -d

check:
	docker-compose exec web python manage.py check

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

migration-check:
	docker-compose exec web python manage.py makemigrations --check --dry-run

verify:
	docker-compose exec web python manage.py check
	docker-compose exec web python manage.py makemigrations --check --dry-run
	docker-compose exec web python manage.py migrate
	docker-compose exec web pytest -v

test:
	docker-compose exec web pytest

shell:
	docker-compose exec web python manage.py shell

superuser:
	docker-compose exec web python manage.py createsuperuser

logs:
	docker-compose logs -f web

celery-logs:
	docker-compose logs -f celery

down:
	docker-compose down
