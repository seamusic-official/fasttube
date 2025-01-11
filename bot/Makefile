install:
	poetry lock
	poetry install


run-local:
	poetry run python -m src.run --reload

lint:
	poetry run flake8
	poetry run mypy -p src --cache-dir=/dev/null --config-file=pyproject.toml
	poetry run mypy -p tests --cache-dir=/dev/null --config-file=pyproject.toml