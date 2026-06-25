from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)

from config.llm import llm

from prompts.repository_prompt import (
    REPOSITORY_PROMPT
)

from tools.github_repo_tool import (
    github_repo_tool
)

from tools.github_readme_tool import (
    github_readme_tool
)

from tools.github_repo_tree_tool import (
    github_repo_tree_tool
)

from tools.github_beginner_issues_tool import (
    github_beginner_issues_tool
)


def repository_node(state):

    repo_url = state["repo_url"]

    # -------------------------
    # GitHub Data Collection
    # -------------------------

    repo_metadata = github_repo_tool.invoke(
        {
            "repo_url": repo_url
        }
    )

    readme_data = github_readme_tool.invoke(
        {
            "repo_url": repo_url
        }
    )

    repo_tree = github_repo_tree_tool.invoke(
        {
            "repo_url": repo_url
        }
    )

    beginner_issues = github_beginner_issues_tool.invoke(
        {
            "repo_url": repo_url
        }
    )

    # -------------------------
    # Repository Analysis
    # -------------------------

    prompt = f"""
{REPOSITORY_PROMPT}

Repository Metadata:

{repo_metadata}

README:

{readme_data}

Repository Structure:

{repo_tree}

Beginner Issues:

{beginner_issues}
"""

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are an expert open source "
                    "repository analyst."
                )
            ),
            HumanMessage(
                content=prompt
            )
        ]
    )

    # -------------------------
    # Save Everything
    # -------------------------

    return {
        "messages": [response],

        "repo_metadata":
            repo_metadata,

        "repo_tree":
            repo_tree,

        "beginner_issues":
            beginner_issues.get(
                "issues",
                []
            ),

        "repository_analysis":
            response.content
    }