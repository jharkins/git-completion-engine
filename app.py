import traceback

from celery import Celery
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from bootstrap import check_redis_connection
from tasks.analyze_commits import analyze_commits

app = Flask(__name__)

redis_ip = 'localhost'
app.config['CELERY_BROKER_URL'] = "amqp://localhost:5672//"
app.config['CELERY_RESULT_BACKEND'] = f'redis://{redis_ip}:6379/0'
app.config['REDIS_URL'] = f'redis://{redis_ip}:6379/0'


def make_celery(app=None):
    if app is None:
        app = Flask(__name__)

    app.config.from_object("config.Config")
    celery = Celery(app.import_name, backend=app.config["CELERY_RESULT_BACKEND"],
                    broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@app.errorhandler(Exception)
def handle_exception(error):
    traceback.print_exc()  # Add this line to print the traceback
    if isinstance(error, HTTPException):
        response = {"error": error.name, "message": error.description}
        status_code = error.code
    else:
        response = {"error": "Internal Server Error", "message": str(error)}
        status_code = 500
    return jsonify(response), status_code


@app.route('/enqueue', methods=['POST'])
def enqueue_job():
    url = request.json['url']
    task = tasks.analyze_commits.apply_async(args=[url, ])
    response = {"job": task.id}
    return jsonify(response), 202


@app.route('/results/<string:job_id>', methods=['GET'])
def get_results(job_id):
    task = tasks.analyze_commits.AsyncResult(job_id)  # Updated task reference
    if task.state == 'PENDING':
        response = {'status': 'PENDING'}
        return jsonify(response), 202
    elif task.state == 'SUCCESS':
        response = {'status': 'SUCCESS', 'data': task.result}
        return jsonify(response), 200
    else:
        response = {'status': 'FAILURE', 'data': str(task.info)}
        return jsonify(response), 500
