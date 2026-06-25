from typing import (
    TypedDict,
    Annotated,
    Optional,
    List,
    Dict,
    Any
)

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):

    # LangGraph conversation history
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

    # User Inputs
    repo_url: Optional[str]
    selected_issue: Optional[int]

    # Raw GitHub Data
    repo_metadata: Optional[Dict[str, Any]]
    repo_tree: Optional[Dict[str, Any]]
    beginner_issues: Optional[List[Dict[str, Any]]]
    issue_details: Optional[Dict[str, Any]]

    # Agent Outputs
    repository_analysis: Optional[str]
    issue_analysis: Optional[str]
    file_mapping_analysis: Optional[str]
    relevant_files: Optional[List[str]]
    issues_dropdown: Optional[List[str]]
    implementation_plan: Optional[str]
    pr_draft: Optional[str]