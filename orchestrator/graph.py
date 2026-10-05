from langgraph.graph import StateGraph, START, END

from orchestrator.state import AgentState
from orchestrator.router import route_question

from orchestrator.nodes.database import (
    get_schema_node,
    generate_sql_node,
    execute_sql_node
)

from orchestrator.nodes.google_search import (
    google_search_node
)

from orchestrator.nodes.final_answer import (
    final_answer_node
)


def build_graph():

    graph = StateGraph(AgentState)

    # =====================================
    # NODES
    # =====================================

    graph.add_node(
        "router",
        route_question
    )

    graph.add_node(
        "get_schema",
        get_schema_node
    )

    graph.add_node(
        "generate_sql",
        generate_sql_node
    )

    graph.add_node(
        "execute_sql",
        execute_sql_node
    )

    graph.add_node(
        "google_search",
        google_search_node
    )

    # IMPORTANT:
    # Run final answer after all other pending work
    # has completed.
    graph.add_node(
        "final_answer",
        final_answer_node,
        defer=True
    )

    # =====================================
    # START → ROUTER
    # =====================================

    graph.add_edge(
        START,
        "router"
    )

    # =====================================
    # ROUTER → MULTIPLE ROUTES
    # =====================================

    graph.add_conditional_edges(
        "router",
        lambda state: state["routes"],
        {
            "database": "get_schema",
            "google_search": "google_search"
        }
    )

    # =====================================
    # DATABASE FLOW
    # =====================================

    graph.add_edge(
        "get_schema",
        "generate_sql"
    )

    graph.add_edge(
        "generate_sql",
        "execute_sql"
    )

    # =====================================
    # DATABASE → FINAL
    # =====================================

    graph.add_edge(
        "execute_sql",
        "final_answer"
    )

    # =====================================
    # GOOGLE → FINAL
    # =====================================

    graph.add_edge(
        "google_search",
        "final_answer"
    )

    # =====================================
    # FINAL → END
    # =====================================

    graph.add_edge(
        "final_answer",
        END
    )

    return graph.compile()