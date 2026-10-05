from typing import TypedDict, Any


class AgentState(TypedDict, total=False):

    question: str

    # Multiple routes
    routes: list[str]

    # Database
    schema: str
    sql: str
    result: Any

    # Google Search
    search_result: Any

    # Final response
    answer: str

    error: str