import os
import shutil
from git import Repo, GitCommandError
from celery import shared_task
from cache import get_cached_data, update_cache


@shared_task(bind=True)
def analyze_commits(self, url):
    parent_dir = "inspection_jobs"
    task_dir = str(self.request.id)
    temp_dir = os.path.join(parent_dir, task_dir)

    cached_data = get_cached_data(url)
    if cached_data:
        print("Using cached data for", url)
        return cached_data

    # Create the parent directory if it doesn't exist
    os.makedirs(parent_dir, exist_ok=True)

    try:
        # Clone the repository to a temporary directory
        repo = Repo.clone_from(url, temp_dir)

        # Get commit messages and diffs
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
        # Remove the temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    update_cache(url, commit_messages, commit_diffs)

    return {"url": url, "commit_messages": commit_messages, "commit_diffs": commit_diffs}
