import os
from github import Github
import re

def get_latest_tags(repo):
    # Fetch all tags from the repository
    tags = repo.get_tags()
    tag_dict = {}
    for tag in tags:
        # Parse the version from the tag name
        match = re.match(r'v(\d+)\.(\d+)\.(\d+)', tag.name)
        if match:
            major, minor, patch = map(int, match.groups())
            tag_dict[tag.name] = {
                'major': major,
                'minor': minor,
                'patch': patch
            }
    return tag_dict

def increment_version(latest_tag_name):

    closed_pr = repo.get_pulls(state='closed')
    closed_pull_request = closed_pr[0]
import re

def get_latest_tags(repo):
    # Fetch all tags from the repository
    tags = repo.get_tags()
    tag_dict = {}
    for tag in tags:
        # Parse the version from the tag name
        match = re.match(r'v(\d+)\.(\d+)\.(\d+)', tag.name)
        if match:
            major, minor, patch = map(int, match.groups())
            tag_dict[tag.name] = {
                'major': major,
                'minor': minor,
                'patch': patch
            }
    return tag_dict

def increment_version(latest_tag_name):

    closed_pr = repo.get_pulls(state='closed')
    closed_pull_request = closed_pr[0]
    branch_name = closed_pull_request.base.ref
    print(branch_name)
    if branch_name.startswith("feature"):
        change_type = "major"
    elif branch_name.startswith("bugfix") or branch_name.startswith("bug_fix"):
       change_type = "minor"
    elif branch_name.startswith("hotfix") or branch_name.startswith("hot_fix"):
       change_type = "patch"
       
    version_numbers = latest_tag_name[1:].split('.')

    # Increment the version numbers based on the change type
    major_increment = 1 if change_type == 'major' else 0
    minor_increment = 1 if change_type == 'minor' else 0
    patch_increment = 1 if change_type == 'patch' else 0

    # Increment the version numbers accordingly
    major_number = int(version_numbers[0]) + major_increment
    minor_number = int(version_numbers[1]) + minor_increment
    patch_number = int(version_numbers[2]) + patch_increment

    # Construct the new tag name
    new_tag_name = f"v{major_number}.{minor_number}.{patch_number}"
    

    return new_tag_name

def fetch_closed_pull_requests(repo):
    # Fetch closed pull requests
    closed_pr = repo.get_pulls(state='closed')
    closed_pull_request = closed_pr[0]
    closed_pr = repo.get_pulls(state='closed')
    closed_pull_request = closed_pr[0]

    # Organize pull requests under different headings
    feature_notes = []
    bug_fix_notes = []
    hot_fix_notes = []
    misc_notes = []


    branch_name = closed_pull_request.base.ref
    if branch_name.startswith("feature"):
        feature_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")
    elif branch_name.startswith("bugfix") or branch_name.startswith("bug_fix"):
        bug_fix_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")
    elif branch_name.startswith("hotfix") or branch_name.startswith("hot_fix"):
        hot_fix_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")
    else:
        misc_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")

    branch_name = closed_pull_request.base.ref
    if branch_name.startswith("feature"):
        feature_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")
    elif branch_name.startswith("bugfix") or branch_name.startswith("bug_fix"):
        bug_fix_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")
    elif branch_name.startswith("hotfix") or branch_name.startswith("hot_fix"):
        hot_fix_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")
    else:
        misc_notes.append(f"@{pull_request.user.login} {pull_request.title} - {pull_request.body}")

# Construct release notes
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

def create_draft_release(repo, release_notes, version):
    # Create a draft release with dynamic tagging
    release = repo.create_git_release(
        tag=version,
        name=f'Release {version}',
        message='Automated release draft',
        draft=True
    )

    # Upload release notes
    release.create_issue_comment(release_notes)

def create_draft_release(repo, release_notes, version):
    # Create a draft release with dynamic tagging
    release = repo.create_git_release(
        tag=version,
        name=f'Release {version}',
        message='Automated release draft',
        draft=True
    )

    # Upload release notes
    release.create_issue_comment(release_notes)

if __name__ == "__main__":
    # Get GitHub token from environment variable
    github_token = os.environ.get('GITHUB_TOKEN')

    # Create a GitHub instance
    g = Github(github_token)

    # Get the repository
    repo = g.get_repo(os.environ.get('GITHUB_REPOSITORY'))

    # Fetch the latest tags and their versions
    tags = repo.get_tags()
    print(tags)


    # Sort the tags based on their creation date (tag.commit.commit.author.date)
    
    try:
        sorted_tags = sorted(tags, key=lambda tag: tag.commit.commit.author.date, reverse=True)
        # Get the name of the latest (most recent) tag
        latest_tag_name = sorted_tags[0].name
    except:
        latest_tag_name = 'v0.0.0'
    
    # Increment the version based on the type of change
    new_version = increment_version(latest_tag_name)  # Example: Incrementing minor version

    # Fetch closed pull requests and generate release notes
    release_notes = fetch_closed_pull_requests(repo)

    # Create a new tag with the updated version
    create_draft_release(repo, release_notes, new_version)

    print(f"Draft release {new_version} created successfully.")
