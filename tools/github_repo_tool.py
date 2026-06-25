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
def github_repo_tool(repo_url: str) -> dict:
    """
    Get repository metadata.
    """

    try:

        parts = repo_url.rstrip("/").split("/")

        owner = parts[-2]
        repo = parts[-1]

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}"
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return {
            "name": data.get("name"),
            "owner": data.get("owner", {}).get("login"),
            "description": data.get("description"),
            "language": data.get("language"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "open_issues": data.get("open_issues_count"),
            "default_branch": data.get("default_branch")
        }

    except Exception as e:

        return {
            "error": str(e)
        }