install:
	poetry install
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl
lint:
	poetry run flake8 flask_example
dev:
	poetry run flask --app flask_example.flask_app --debug run --port 8000
routes:
	poetry run flask --app flask_example.flask_app routes
start:
	poetry run python -m gunicorn -w 5 flask_example.flask_app:app