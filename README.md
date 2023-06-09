# Git Completion Engine

A simple implementation of an idea to check git commits a human makes vs a GPT engine.

Git Completion Engine is a Python-based application that analyzes the commit history of a given Git repository. It uses Flask, Celery, and Redis to provide an asynchronous API for enqueueing analysis tasks and fetching results.

## Features

- Asynchronous processing of Git repositories
- Retrieve commit messages and diffs

## Getting Started

These instructions will help you set up and run the Git Completion Engine on your local machine.

### Prerequisites

- Python 3.7+
- Redis
- RabbitMQ
- Docker (optional, for running RabbitMQ and Redis in containers)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/jharkins/git-completion-engine.git
```

2. Change into the project directory:

```bash
cd git-completion-engine
```

3. Set up a virtual environment and install dependencies:

```bash
make setup
```

4. Start RabbitMQ and Redis services (using Docker):

```bash
make start-rabbitmq
make start-redis
```

5. Run the Flask application:

```bash
make run-app
```

6. In a separate terminal, run the Celery worker:

```bash
make run-celery
```

## Usage

1. Enqueue a Git repository for analysis:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://github.com/jharkins/repository.git"}' http://localhost:5000/enqueue
```

2. Check the status of the analysis and fetch the results:

```bash
curl http://localhost:5000/results/<job_id>
```

Replace `<job_id>` with the job ID returned in the response of the previous command.

## enqueue_and_wait.py

`enqueue_and_wait.py` is a command-line utility that enqueues a job to analyze a Git repository using analyze_commits() task and then waits for the result to be available. It takes a single argument, which is the URL of the Git repository to analyze. Here's an example usage:

```bash
$ python enqueue_and_wait.py https://github.com/username/repo.git
```

When you run the script, it first enqueues the job by calling analyze_commits.apply_async() and then waits for the job to complete by polling the task status using AsyncResult(). When the task completes, it prints the result to the console.

The enqueue_and_wait.py script depends on the analyze_commits() task, which is defined in tasks.py, and the make_celery() function, which is defined in app.py. It also uses the Celery library and the celery.result.AsyncResult class to manage tasks and retrieve results.

## Contributors

- Joe Harkins - [GitHub](https://github.com/jharkins)
- ChatGPT by OpenAI - [Website](https://openai.com)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/jharkins/git-completion-engine/blob/master/LICENSE.md) file for details.
