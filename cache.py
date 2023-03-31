# cache.py
import os
import pickle

CACHE_FILE = "commit_cache.pkl"


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return {}


def save_cache(cache):
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)


def update_cache(url, commit_messages, commit_diffs):
    cache = load_cache()
    cache[url] = {"commit_messages": commit_messages,
                  "commit_diffs": commit_diffs}
    save_cache(cache)


def get_cached_data(url):
    cache = load_cache()
    return cache.get(url)
