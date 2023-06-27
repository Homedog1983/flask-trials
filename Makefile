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
kill-8000:
	npx kill-port 8000
dev:
	poetry run flask --app flask_example.flask_app --debug run --port 8000
routes:
	poetry run flask --app flask_example.flask_app routes
gunicorn:
	poetry run python -m gunicorn -w 5 flask_example.flask_app:app
