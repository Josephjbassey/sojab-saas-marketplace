.PHONY: init dev test shell migrations migrate

init:
	cp .env.example .env
	docker compose -f docker-compose.example.yml up -d db redis
	# Run migrations and create superuser manually or via seed script

dev:
	docker compose -f docker-compose.example.yml up

test:
	pytest

shell:
	python manage.py shell

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate
