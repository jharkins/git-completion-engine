import os
import shutil
from git import Repo, GitCommandError
from celery import shared_task
from cache import get_cached_data, update_cache


def get_commit_messages(url, task_id=None):
    parent_dir = "inspection_jobs"
    os.makedirs(parent_dir, exist_ok=True)

    temp_dir = os.path.join(
        parent_dir, task_id) if task_id else os.path.join(parent_dir, "temp")

    cached_data = get_cached_data(url)
    if cached_data:
        print("Using cached data for", url)
        return cached_data

    try:
        repo = Repo.clone_from(url, temp_dir)

        commit_messages = []
        commit_diffs = []
        for commit in repo.iter_commits():
            commit_messages.append(commit.message)

            diffs = []
            parent_commit = commit.parents[0] if commit.parents else None
            for diff in commit.diff(parent_commit, create_patch=True):
                diffs.append(diff.diff.decode('utf-8'))

            commit_diffs.append(diffs)

    except GitCommandError as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    update_cache(url, commit_messages, commit_diffs)

    return {"url": url, "commit_messages": commit_messages, "commit_diffs": commit_diffs}


@shared_task(bind=True)
def analyze_commits(self, url):
    task_id = str(self.request.id)
    commits = get_commit_messages(url, task_id)

    if "commit_messages" in commits:
        for message in commits["commit_messages"]:
            print(message)

    return commits
