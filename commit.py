class Commit:
    def __init__(self, commit_hash, message, diff, summary=None):
        self.commit_hash = commit_hash
        self.message = message
        self.diff = diff
        self.summary = summary

    def __repr__(self):
        return f"Commit(hash={self.commit_hash}, message={self.message}, summary={self.summary})"
