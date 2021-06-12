run:
	poetry run python run.py

pytest:
	poetry run pytest

lint:
	poetry run flake8

format:
	poetry run black .
	poetry run isort .

install-hooks:
	poetry run pre-commit install -t pre-commit
	poetry run pre-commit install -t pre-push
