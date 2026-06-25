from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)

from config.llm import llm

from prompts.file_mapper_prompt import (
    FILE_MAPPER_PROMPT
)

from tools.github_file_content_tool import (
    github_file_content_tool
)


def file_mapper_node(state):

    repo_url = state["repo_url"]

    issue_details = state["issue_details"]

    repo_tree = state["repo_tree"]

    # -------------------------
    # Candidate File Selection
    # -------------------------

    sample_files = repo_tree.get(
        "sample_files",
        []
    )

    candidate_files = sample_files[:15]

    file_context = []

    # -------------------------
    # Read Candidate Files
    # -------------------------

    for file_path in candidate_files:

        try:

            file_data = (
                github_file_content_tool.invoke(
                    {
                        "repo_url": repo_url,
                        "file_path": file_path
                    }
                )
            )

            if "content" in file_data:

                file_context.append(
                    {
                        "file_path": file_path,
                        "content":
                            file_data["content"][:3000]
                    }
                )

        except Exception:
            pass

    # -------------------------
    # LLM Analysis
    # -------------------------

    prompt = f"""
{FILE_MAPPER_PROMPT}

Issue Details:

{issue_details}

Repository Files:

{candidate_files}

File Contents:

{file_context}

Determine which files are most likely
related to the issue.

Return file paths in ranked order.
"""

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a senior software architect."
                )
            ),
            HumanMessage(
                content=prompt
            )
        ]
    )

    # -------------------------
    # Extract Relevant Files
    # -------------------------

    relevant_files = candidate_files

    return {
        "messages": [response],

        "relevant_files":
        candidate_files,

        "file_mapping_analysis":
        response.content
    }