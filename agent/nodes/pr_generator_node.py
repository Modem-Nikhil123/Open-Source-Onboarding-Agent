from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)

from config.llm import llm

from prompts.pr_prompt import (
    PR_PROMPT
)


def pr_generator_node(state):

    repo_metadata = state["repo_metadata"]

    issue_details = state["issue_details"]

    issue_analysis = state["issue_analysis"]

    relevant_files = state["relevant_files"]

    implementation_plan = (
        state["implementation_plan"]
    )

    prompt = f"""
{PR_PROMPT}

Repository Metadata:

{repo_metadata}

Issue Details:

{issue_details}

Issue Analysis:

{issue_analysis}

Relevant Files:

{relevant_files}

Implementation Plan:

{implementation_plan}

Generate:

1. Branch Name

2. Commit Message

3. PR Title

4. Professional PR Description

Make it look like a real pull request.
"""

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are an experienced open source maintainer."
                )
            ),
            HumanMessage(
                content=prompt
            )
        ]
    )

    return {
        "messages": [response],

        "pr_draft":
            response.content
    }