import os
import shutil
from git import Repo, GitCommandError
from celery import shared_task


@shared_task
def clone_repo_task(url, temp_dir):
    repo = Repo.clone_from(url, temp_dir)

    commit_data = []
    for commit in repo.iter_commits():
        message = commit.message

        diffs = []
        parent_commit = commit.parents[0] if commit.parents else None
        for diff in commit.diff(parent_commit, create_patch=True):
            diffs.append(diff.diff.decode('utf-8'))

        commit_data.append({"commit_message": message, "commit_diffs": diffs})

    return commit_data
