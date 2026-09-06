.PHONY: install lint format test check migrate run

install:
	python -m pip install -r requirements/dev.txt

lint:
	ruff check .

format:
	ruff format .
	ruff check --fix .

test:
	pytest

check:
	python manage.py check

migrate:
	python manage.py migrate

run:
	python manage.py runserver
