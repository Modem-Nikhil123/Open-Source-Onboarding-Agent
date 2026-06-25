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
def github_repo_tree_tool(repo_url: str) -> dict:
    """
    Fetch repository structure.
    """

    try:

        parts = repo_url.rstrip("/").split("/")

        owner = parts[-2]
        repo = parts[-1]

        repo_url_api = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}"
        )

        repo_response = requests.get(
            repo_url_api,
            headers=HEADERS,
            timeout=30
        )

        repo_response.raise_for_status()

        default_branch = (
            repo_response.json()
            .get("default_branch", "main")
        )

        tree_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/git/trees/"
            f"{default_branch}"
            f"?recursive=1"
        )

        tree_response = requests.get(
            tree_url,
            headers=HEADERS,
            timeout=30
        )

        tree_response.raise_for_status()

        tree_data = tree_response.json()

        files = []

        for item in tree_data["tree"]:

            if item["type"] == "blob":
                files.append(item["path"])

        top_level_folders = sorted(
            list(
                {
                    path.split("/")[0]
                    for path in files
                    if "/" in path
                }
            )
        )

        return {
            "total_files": len(files),
            "top_level_folders": top_level_folders[:50],
            "sample_files": files[:200]
        }

    except Exception as e:

        return {
            "error": str(e)
        }