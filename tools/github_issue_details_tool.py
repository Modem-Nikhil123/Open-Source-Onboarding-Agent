import os
import requests

from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


@tool
def github_issue_details_tool(
    repo_url: str,
    issue_number: int
) -> dict:
    """
    Get issue details.
    """

    try:

        parts = repo_url.rstrip("/").split("/")

        owner = parts[-2]
        repo = parts[-1]

        issue_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/issues/"
            f"{issue_number}"
        )

        response = requests.get(
            issue_url,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        issue = response.json()

        return {
            "number": issue["number"],
            "title": issue["title"],
            "body": issue.get("body", ""),
            "state": issue["state"],
            "labels": [
                label["name"]
                for label in issue["labels"]
            ],
            "comments": issue["comments"],
            "url": issue["html_url"]
        }

    except Exception as e:

        return {
            "error": str(e)
        }