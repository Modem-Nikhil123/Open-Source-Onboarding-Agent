import sqlite3
from pathlib import Path

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

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "onboarding.db"

conn = sqlite3.connect(
    str(DB_PATH),
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