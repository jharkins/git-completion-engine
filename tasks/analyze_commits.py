import os
import shutil
from git import GitCommandError
from celery import shared_task, group
from .clone_repo import clone_repo_task
from .generate_summary import generate_summary_task
from cache import get_cached_data, update_cache
from commit import Commit


@shared_task(bind=True)
def analyze_commits(self, url):
    parent_dir = "inspection_jobs"
    task_dir = str(self.request.id)
    temp_dir = os.path.join(parent_dir, task_dir)

    cached_data = get_cached_data(url)
    if cached_data:
        print("Using cached data for", url)
        return cached_data

    os.makedirs(parent_dir, exist_ok=True)

    try:
        commit_data = clone_repo_task(url, temp_dir)

        summary_tasks = group(generate_summary_task.s(
            commit.diff) for commit in commit_data)
        summaries = summary_tasks.apply_async().get()

        for idx, commit in enumerate(commit_data):
            commit.summary = summaries[idx]

    except GitCommandError as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    update_cache(url, commit_data)

    for commit in commit_data:
        print(f"Commit message: {commit.message}")
        print(f"Summary: {commit.summary}")

    return {"url": url, "commit_data": commit_data}
