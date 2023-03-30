.PHONY: help setup run-app run-celery start-rabbitmq start-redis stop-rabbitmq stop-redis

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  setup          to create a virtual environment and install dependencies"
	@echo "  run-app        to run the Flask app"
	@echo "  run-celery     to run the Celery worker"
	@echo "  start-rabbitmq to start RabbitMQ in a Docker container"
	@echo "  start-redis    to start Redis in a Docker container"
	@echo "  stop-rabbitmq  to stop the RabbitMQ Docker container"
	@echo "  stop-redis     to stop the Redis Docker container"

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

run-app:
	. venv/bin/activate && export FLASK_APP=app.py && export FLASK_DEBUG=true && flask run

run-celery:
	. venv/bin/activate && celery -A app.celery worker --loglevel=info

start-rabbitmq:
	docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

start-redis:
	docker run -d --name redis -p 6379:6379 redis:latest

stop-rabbitmq:
	docker stop rabbitmq && docker rm rabbitmq

stop-redis:
	docker stop redis && docker rm redis

.PHONY: test-api
test-api:
	curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com"}' http://localhost:5000/enqueue
