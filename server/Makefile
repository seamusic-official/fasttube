install:
	poetry install

run-local:
	poetry run alembic upgrade head
	poetry run uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload --reload-dir . --log-config=log_config.ini --log-level=debug

revision:
	poetry run docker run app /bin/bash -c "poetry run alembic revision --autogenerate"

upgrade:
	poetry run docker run app /bin/bash -c "poetry run alembic upgrade $(revision)"

downgrade:
	poetry run docker run app /bin/bash -c "poetry run alembic downgrade $(revision)"

lint:
	poetry run flake8
	poetry run mypy -p src --cache-dir=/dev/null --config-file=pyproject.toml
	poetry run mypy -p tests --cache-dir=/dev/null --config-file=pyproject.toml
