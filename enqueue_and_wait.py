import time
import sys
from tasks.analyze_commits import analyze_commits
from celery.result import AsyncResult
from app import make_celery
from pprint import pprint


def main():
    if len(sys.argv) < 2:
        print("Usage: python enqueue_and_wait.py <git_repository_url>")
        return

    git_url = sys.argv[1]

    # Enqueue the job
    task = analyze_commits.apply_async(args=[git_url])

    print(f"Enqueued task with ID: {task.task_id}")

    # Wait for the task to finish
    while not task.ready():
        time.sleep(1)

    # Get the result
    result = AsyncResult(task.task_id, app=make_celery())

    if result.successful():
        print("Task completed successfully!")
        print("Result:")
        pprint(result.result)
    else:
        print("Task failed:")
        pprint(result.result)


if __name__ == "__main__":
    main()
