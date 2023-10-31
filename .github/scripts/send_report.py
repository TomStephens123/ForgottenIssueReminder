import os
import requests
from collections import defaultdict

GITHUB_API_URL = "https://api.github.com" #TODO
SLACK_API_URL = "https://slack.com/api" #TODO

def get_issues(org, repo, token):
    url = f"{GITHUB_API_URL}/repos/{org}/{repo}/issues"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching issues: {response.status_code}")
        return []

def group_issues_by_assignee(issues):
    grouped_issues = defaultdict(list)
    for issue in issues:
        assignee = issue.get('assignee', {}).get('login', 'Unassigned')
        labels = [label['name'] for label in issue.get('labels', [])]
        grouped_issues[assignee].append((issue['title'], labels))
    return grouped_issues

def format_message(grouped_issues):
    message = "Weekly GitHub Issues Report:\n"
    for assignee, issues in grouped_issues.items():
        message += f"\n{assignee}:\n"
        for title, labels in issues:
            message += f"  - {title} ({', '.join(labels)})\n"
    return message

def send_slack_message(token, channel, text):
    url = f"{SLACK_API_URL}/chat.postMessage"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"channel": channel, "text": text}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Error sending message: {response.status_code}")

def main():
    github_token = os.getenv("GITHUB_TOKEN")
    slack_token = os.getenv("SLACK_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL")
    repo = os.getenv("REPOSITORY")
    org = os.getenv("ORGANIZATION")

    issues = get_issues(org, repo, github_token)
    grouped_issues = group_issues_by_assignee(issues)
    message = format_message(grouped_issues)
    send_slack_message(slack_token, slack_channel, message)

if __name__ == "__main__":
    main()
