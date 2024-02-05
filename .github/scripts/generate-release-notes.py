import os
from github import Github

def fetch_closed_pull_requests():
    # Get GitHub token from environment variable
    github_token = os.environ.get('GITHUB_TOKEN')

    # Create a GitHub instance
    g = Github(github_token)

    # Get the repository
    repo = g.get_repo(os.environ.get('GITHUB_REPOSITORY'))

    # Fetch closed pull requests
    closed_pull_requests = repo.get_pulls(state='closed')

    # Organize pull requests under different headings
    feature_notes = []
    bug_fix_notes = []
    hot_fix_notes = []
    misc_notes = []

    for pull_request in closed_pull_requests:
        # Determine the branch type
        branch_name = pull_request.base.ref
        if branch_name.startswith("feature"):
            feature_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")
        elif branch_name.startswith("bugfix") or branch_name.startswith("bug_fix"):
            bug_fix_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")
        elif branch_name.startswith("hotfix") or branch_name.startswith("hot_fix"):
            hot_fix_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")
        else:
            misc_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")

    # Construct release notes
    release_notes = "## Changes\n\n"
    if feature_notes:
        release_notes += "### 🚀 Features\n"
        release_notes += "\n".join(feature_notes) + "\n\n"
    if bug_fix_notes:
        release_notes += "### 🐛 Bug Fixes\n"
        release_notes += "\n".join(bug_fix_notes) + "\n\n"
    if hot_fix_notes:
        release_notes += "### 🧰 Hot Fixes\n"
        release_notes += "\n".join(hot_fix_notes) + "\n\n"
    if misc_notes:
        release_notes += "### 🧺 Miscellaneous\n"
        release_notes += "\n".join(misc_notes) + "\n\n"

    return release_notes

if __name__ == "__main__":
    release_notes = fetch_closed_pull_requests()
    print(release_notes)
