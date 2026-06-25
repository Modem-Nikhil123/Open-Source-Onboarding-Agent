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
def github_beginner_issues_tool(
    repo_url: str
) -> dict:
    """
    Fetch beginner-friendly issues.
    """

    try:

        parts = repo_url.rstrip("/").split("/")

        owner = parts[-2]
        repo = parts[-1]

        labels = [
            "good first issue",
            "good-first-issue",
            "beginner",
            "easy",
            "help wanted"
        ]

        issues = []
        seen = set()

        for label in labels:

            url = (
                f"https://api.github.com/repos/"
                f"{owner}/{repo}/issues"
            )

            response = requests.get(
                url,
                headers=HEADERS,
                params={
                    "state": "open",
                    "labels": label,
                    "per_page": 20
                },
                timeout=30
            )

            if response.status_code != 200:
                continue

            for issue in response.json():

                if "pull_request" in issue:
                    continue

                if issue["number"] in seen:
                    continue

                seen.add(
                    issue["number"]
                )

                issues.append(
                    {
                        "number": issue["number"],
                        "title": issue["title"],
                        "url": issue["html_url"],
                        "labels": [
                            label["name"]
                            for label in issue["labels"]
                        ]
                    }
                )

        return {
            "count": len(issues),
            "issues": issues[:20]
        }

    except Exception as e:

        return {
            "error": str(e)
        }