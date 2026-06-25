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
def github_readme_tool(repo_url: str) -> dict:
    """
    Get README content.
    """

    try:

        parts = repo_url.rstrip("/").split("/")

        owner = parts[-2]
        repo = parts[-1]

        readme_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/readme"
        )

        response = requests.get(
            readme_url,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        download_url = (
            response.json()["download_url"]
        )

        content = requests.get(
            download_url,
            timeout=30
        ).text

        return {
            "content": content[:15000]
        }

    except Exception as e:

        return {
            "error": str(e)
        }