.PHONY: help setup run-app run-celery

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  setup          to create a virtual environment and install dependencies"
	@echo "  run-app        to run the Flask app"
	@echo "  run-celery     to run the Celery worker"

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

run-app:
	. venv/bin/activate && export FLASK_APP=app.py && export FLASK_DEBUG=true && flask run

run-celery:
	. venv/bin/activate && celery -A app.celery worker --loglevel=info

.PHONY: test-api
test-api:
	curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://localhost:5000/enqueue
