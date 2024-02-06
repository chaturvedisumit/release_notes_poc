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
    print("branch_name",branch_name)
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

    pull_request_url = closed_pull_request.html_url

    commits = closed_pull_request.get_commits()
    
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

        # Append the link to the pull request to your feature_notes
        misc_notes.append(f"Pull Request: {pull_request_url}")

        # Add commit messages
        for commit in commits:
            misc_notes.append(f"Commit: {commit.sha[:7]} - {commit.commit.message}")

# Construct release notes
    release_notes = ""
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

    print ("older:",release_notes)
    return release_notes

def group_release_info(release_notes):
    # Split the release notes into sections based on section titles
    sections = re.split(r'(?:^|\n)#{2,3}\s+', release_notes.strip())

    # Initialize a dictionary to store sections
    grouped_info = {}
    
    # Process each section
    for section in sections:
        if section.strip():
            # Split each section into title and content
            lines = section.strip().split('\n')
            section_title = lines[0].strip()
            section_content = '\n'.join(lines[1:]).strip()

            # Add section content to the corresponding title in the dictionary
            if section_title in grouped_info:
                grouped_info[section_title].append(section_content)
            else:
                grouped_info[section_title] = [section_content]

    return grouped_info





def create_draft_release(repo, release_notes, version):
    # Get the latest release
    latest_release = repo.get_releases()[0]

    # Get the body of the latest release
    release_body = latest_release.body

    # Merge the old body with the new release notes
    merged_message = release_body + '\n\n' + release_notes

    print("merged_message:", merged_message)

    # Format the merged message using group_release_info()
    formatted_message = ""
    grouped_info = group_release_info(merged_message)
    print("grouped_info:", grouped_info)
    # Format the merged message using group_release_info()
    formatted_message = ""
    for section, notes in grouped_info.items():
        formatted_message += f"## {section}\n"
        for note in notes:
            formatted_message += f"- {note}\n"
        formatted_message += "\n"


    print("formatted_message:", formatted_message)


    # Update the release with the formatted message and keep it as a draft
    latest_release.update_release(
        name=latest_release.title,
        message=formatted_message,
        draft=True
    )

    return formatted_message





if __name__ == "__main__":
    # Get GitHub token from environment variable
    github_token = os.environ.get('GITHUB_TOKEN')

    # Create a GitHub instance
    g = Github(github_token)

    # Get the repository
    repo = g.get_repo(os.environ.get('GITHUB_REPOSITORY'))

    # Fetch the latest tags and their versions
    tags = repo.get_tags()
    print("tags: ", tags)

    latest_draft_tag = os.environ.get('DRAFT_RELEASE_TAG_NUMBER')
    latest_tag = os.environ.get('LATEST_TAG')
    
    # Increment the version based on the type of change
    if latest_draft_tag <> null :
        new_version = increment_version(latest_draft_tag)  # Example: Incrementing minor version
    elif latest_tag <> null :
        new_version = increment_version(latest_tag)
    else:
        new_version = "v0.0.0"

    # Fetch closed pull requests and generate release notes
    release_notes = fetch_closed_pull_requests(repo)

    # Create a new tag with the updated version
    release_notes_final = create_draft_release(repo, release_notes, new_version)

    # Check if an existing draft release exists
    latest_release = repo.get_releases()[0]
    
    
    # If an existing draft release is found, create a new draft release and delete the existing one
   
    # Create a new draft release from the updated one
    new_draft_release = repo.create_git_release(
        tag=new_version,
        name=new_version,
        message=release_notes_final,
        draft=True
    )

    print("new_draft_release", new_draft_release)

        # Delete the existing draft release
    latest_release.delete_release()

    print(f"Draft release {new_version} created successfully.")
  
