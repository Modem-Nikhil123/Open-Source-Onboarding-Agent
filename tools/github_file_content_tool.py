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
def github_file_content_tool(
    repo_url: str,
    file_path: str
) -> dict:
    """
    Read repository file content.
    """

    try:

        parts = repo_url.rstrip("/").split("/")

        owner = parts[-2]
        repo = parts[-1]

        url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/contents/"
            f"{file_path}"
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        download_url = (
            data.get("download_url")
        )

        if not download_url:

            return {
                "error":
                "Download URL not found"
            }

        content = requests.get(
            download_url,
            timeout=30
        ).text

        return {
            "file_path": file_path,
            "content": content[:15000]
        }

    except Exception as e:

        return {
            "error": str(e)
        }