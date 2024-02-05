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
    
    labels = closed_pull_request.get_labels()
    branch_name = [label.name for label in labels][0].strip()

    print("branch_name:",branch_name)
    if branch_name=="feature":
        change_type = "major"
    elif branch_name=="bugfix" or branch_name == "bug_fix":
       change_type = "minor"
    elif branch_name=="hotfix" or branch_name=="hot_fix":
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

    print("closed_pr: ", closed_pr)

    closed_pull_request = closed_pr[0]
    


    print("closed_pull_request: ", closed_pull_request)

    labels = closed_pull_request.get_labels()
    branch_name = [label.name for label in labels][0]


    # Organize pull requests under different headings
    feature_notes = []
    bug_fix_notes = []
    hot_fix_notes = []
    misc_notes = []
    
    if branch_name=="feature":
        feature_notes.append(f"@{closed_pull_request.user.login} {closed_pull_request.title} - {closed_pull_request.body}")

        # Append the link to the pull request to your feature_notes
        feature_notes.append(f"Pull Request: {pull_request_url}")

        # Add commit messages
        for commit in commits:
            feature_notes.append(f"Commit: {commit.sha[:7]} - {commit.commit.message}")

# Now feature_notes contains the pull request URL, pull request title, body, and commit messages

    elif branch_name=="bugfix" or branch_name=="bug_fix":
        bug_fix_notes.append(f"@{closed_pull_request.user.login} {closed_pull_request.title} - {closed_pull_request.body}")

        bug_fix_notes.append(f"@{closed_pull_request.user.login} {closed_pull_request.title} - {closed_pull_request.body}")
        # Fetch the URL of the pull request


        # Append the link to the pull request to your feature_notes
        bug_fix_notes.append(f"Pull Request: {pull_request_url}")

        # Add commit messages
        for commit in commits:
            bug_fix_notes.append(f"Commit: {commit.sha[:7]} - {commit.commit.message}")


    elif branch_name=="hotfix" or branch_name=="hot_fix":

        hot_fix_notes.append(f"@{closed_pull_request.user.login} {closed_pull_request.title} - {closed_pull_request.body}")

        # Append the link to the pull request to your feature_notes
        hot_fix_notes.append(f"Pull Request: {pull_request_url}")

        # Add commit messages
        for commit in commits:
            hot_fix_notes.append(f"Commit: {commit.sha[:7]} - {commit.commit.message}")

    else:
        misc_notes.append(f"@{closed_pull_request.user.login} {closed_pull_request.title} - {closed_pull_request.body}")

        misc_notes.append(f"@{closed_pull_request.user.login} {closed_pull_request.title} - {closed_pull_request.body}")

        misc_notes.append(f"@{closed_pull_request.user.login} {closed_pull_request.title} - {closed_pull_request.body}")

        # Append the link to the pull request to your feature_notes
        misc_notes.append(f"Pull Request: {pull_request_url}")

        # Add commit messages
        for commit in commits:
            misc_notes.append(f"Commit: {commit.sha[:7]} - {commit.commit.message}")

# Construct release notes
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

    print (release_notes)
    return release_notes

def group_release_info(release_notes):
    # Split the release notes into sections based on headings
    sections = release_notes.split("## ")[1:]

    # Initialize a dictionary to store sections
    grouped_info = {}

    # Process each section
    for section in sections:
        # Split each section into title and content
        section_title, section_content = section.split("\n", 1)

        # Remove leading and trailing whitespace from title
        section_title = section_title.strip()

        # Add section content to the corresponding title in the dictionary
        if section_title in grouped_info:
            grouped_info[section_title].append(section_content)
        else:
            grouped_info[section_title] = [section_content]

    return grouped_info


def create_draft_release(repo, release_notes, version):
    # Create a draft release with dynamic tagging
    
    latest_release = repo.get_releases()[0]
    release_body = latest_release.body
    print(type(release_body))
    print(release_body)

    release = repo.create_git_release(
        tag=version,
        name=f'Release {version}',
        message = release_body,
        draft=True
    )

    release_notes_merged = release.body + '\n\n' + release_notes

    message = group_release_info(release_notes_merged)

    # Upload release notes
    release.update_release(
        name=release.title,
        message=message,
        draft=True
    )

    # Delete the old release
    latest_release.delete_release()



if __name__ == "__main__":
    # Get GitHub token from environment variable
    github_token = os.environ.get('GITHUB_TOKEN')

    # Create a GitHub instance
    g = Github(github_token)

    # Get the repository
    repo = g.get_repo(os.environ.get('GITHUB_REPOSITORY'))

    # Fetch the latest tags and their versions
    tags = repo.get_tags()
    print("tags: ",tags)


    # Sort the tags based on their creation date (tag.commit.commit.author.date)
    
    # try:
    #     sorted_tags = sorted(tags, key=lambda tag: tag.commit.commit.author.date, reverse=True)
    #     # Get the name of the latest (most recent) tag
    #     latest_tag_name = sorted_tags[0].name
    # except:
    #     latest_tag_name = 'v0.0.0' 
    
    latest_tag_name= os.environ.get('DRAFT_RELEASE_TAG_NUMBER')
    # Increment the version based on the type of change
    new_version = increment_version(latest_tag_name)  # Example: Incrementing minor version

    # Fetch closed pull requests and generate release notes
    release_notes = fetch_closed_pull_requests(repo)

    # Create a new tag with the updated version
    release_notes_final = create_draft_release(repo, release_notes, new_version)

    group_release_info(release_notes_final)

    print(f"Draft release {new_version} created successfully.")