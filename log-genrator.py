import git
from datetime import datetime

def parse_commit_message(message):
    parts = message.split(": ", 1)
    if len(parts) != 2:
        return None, None
    commit_type, description = parts
    return commit_type, description

def generate_changelog(repo_path):
    repo = git.Repo(repo_path)
    commits = list(repo.iter_commits('master'))  # Replace 'main' with your branch name if different
    changelog = {
        "feat": [],
        "fix": [],
        "chore": [],
        "docs": [],
        "style": [],
        "refactor": [],
        "perf": [],
        "test": [],
        "build": [],
        "ci": [],
        "revert": []
    }

    for commit in commits:
        commit_type, description = parse_commit_message(commit.message)
        if commit_type and (commit_type in changelog):
            print('commit_type:',commit_type)
            changelog[commit_type].append({
                "description": description,
                "hash": commit.hexsha,
                "date": datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d')
            })

    return changelog

def write_changelog(changelog, filepath):
    with open(filepath, 'w') as f:
        f.write("# Changelog\n\n")
        for commit_type, entries in changelog.items():
            if entries:
                f.write(f"## {commit_type.capitalize()}\n\n")
                for entry in entries:
                    f.write(f"- {entry['date']} [{entry['hash'][:7]}] - {entry['description']}\n")
                f.write("\n")

if __name__ == "__main__":
    repo_path = "."  # Path to your git repository
    changelog = generate_changelog(repo_path)
    write_changelog(changelog, "CHANGELOG.md")
    print("Changelog generated and saved to CHANGELOG.md")

