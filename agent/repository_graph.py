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

from agent.nodes.repository_node import (
    repository_node
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
    "repository_node",
    repository_node
)

graph.add_edge(
    START,
    "repository_node"
)

graph.add_edge(
    "repository_node",
    END
)

repository_graph = graph.compile(
    checkpointer=checkpointer
)