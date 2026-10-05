from orchestrator.mcpclient import call_mcp_tool
from orchestrator.state import AgentState


async def google_search_node(state: AgentState):

    question = state["question"]

    print("\nSearching the web...")

    # Create a focused web-search query
    search_query = f"""
    current market availability of Dettol soap Ice flavour
    Sandle flavour soap availability
    """

    print(f"Google search query: {search_query.strip()}")

    result = await call_mcp_tool(
        "google_search",
        "search_google",
        {
            "query": search_query.strip()
        }
    )

    print("\nRAW GOOGLE SEARCH RESULT:")
    print(result)

    print("\nGoogle Search completed.")

    return {
        "search_result": result
    }