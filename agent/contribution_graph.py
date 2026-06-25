import sqlite3

from langgraph.graph import (
    START,
    END,
    StateGraph
)

from langgraph.checkpoint.sqlite import (
    SqliteSaver
)

from models.state import (
    AgentState
)

from agent.nodes.issue_analysis_node import (
    issue_analysis_node
)

from agent.nodes.file_mapper_node import (
    file_mapper_node
)

from agent.nodes.implementation_node import (
    implementation_node
)

from agent.nodes.pr_generator_node import (
    pr_generator_node
)


conn = sqlite3.connect(
    "database/onboarding.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(
    conn=conn
)

graph = StateGraph(
    AgentState
)

graph.add_node(
    "issue_analysis_node",
    issue_analysis_node
)

graph.add_node(
    "file_mapper_node",
    file_mapper_node
)

graph.add_node(
    "implementation_node",
    implementation_node
)

graph.add_node(
    "pr_generator_node",
    pr_generator_node
)

graph.add_edge(
    START,
    "issue_analysis_node"
)

graph.add_edge(
    "issue_analysis_node",
    "file_mapper_node"
)

graph.add_edge(
    "file_mapper_node",
    "implementation_node"
)

graph.add_edge(
    "implementation_node",
    "pr_generator_node"
)

graph.add_edge(
    "pr_generator_node",
    END
)

contribution_graph = graph.compile(
    checkpointer=checkpointer
)