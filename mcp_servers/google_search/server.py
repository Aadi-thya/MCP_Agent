import asyncio

from ddgs import DDGS
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("google-search")


@mcp.tool()
async def search_google(query: str) -> str:
    """
    Search the web for the given query and return relevant results.
    """
    if not query.strip():
        return "Search query cannot be empty."

    try:
        # ddgs is synchronous, so run it in a thread
        results = await asyncio.to_thread(
            lambda: list(DDGS().text(query, max_results=5))
        )
    except Exception as e:
        return f"Search failed: {e}"

    if not results:
        return f"No search results found for: {query}"

    return "\n\n".join(
        f"Title: {r.get('title', '')}\n"
        f"Summary: {r.get('body', '')}\n"
        f"URL: {r.get('href', '')}"
        for r in results
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")