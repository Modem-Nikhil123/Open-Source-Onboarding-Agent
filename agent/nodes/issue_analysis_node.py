from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)

from config.llm import llm

from prompts.issue_prompt import (
    ISSUE_PROMPT
)

from tools.github_issue_details_tool import (
    github_issue_details_tool
)


def issue_analysis_node(state):

    repo_url = state["repo_url"]

    issue_number = state["selected_issue"]

    # -------------------------
    # Fetch Issue
    # -------------------------

    issue_details = github_issue_details_tool.invoke(
        {
            "repo_url": repo_url,
            "issue_number": issue_number
        }
    )

    # -------------------------
    # Analyze Issue
    # -------------------------

    prompt = f"""
{ISSUE_PROMPT}

Issue Details:

{issue_details}
"""

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are an experienced "
                    "open source mentor."
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

        "issue_details":
            issue_details,

        "issue_analysis":
            response.content
    }