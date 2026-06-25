from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)

from config.llm import llm

from prompts.implementation_prompt import (
    IMPLEMENTATION_PROMPT
)


def implementation_node(state):

    repo_metadata = state["repo_metadata"]

    issue_details = state["issue_details"]

    issue_analysis = state["issue_analysis"]

    relevant_files = state.get(
    "relevant_files",
    []
    )

    file_mapping_analysis = state.get(
    "file_mapping_analysis",
    ""
    )

    prompt = f"""
{IMPLEMENTATION_PROMPT}

Repository Metadata:

{repo_metadata}

Issue Details:

{issue_details}

Issue Analysis:

{issue_analysis}

File Mapping Analysis:

{file_mapping_analysis}

Relevant Files:

{relevant_files}

Generate a detailed implementation plan.

Be specific.

Reference likely code changes.

Reference likely test updates.
"""

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a senior software engineer "
                    "reviewing an open source issue."
                )
            ),
            HumanMessage(
                content=prompt
            )
        ]
    )

    return {
        "messages": [response],

        "implementation_plan":
            response.content
    }