from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATHS = {
    "database": r".\mcp_servers\database\server.py",
    "google_search": r".\mcp_servers\google_search\server.py",
}


def create_server_params(server_name: str):

    if server_name not in SERVER_PATHS:
        raise ValueError(
            f"Unknown MCP server: {server_name}"
        )

    return StdioServerParameters(
        command="uv",
        args=[
            "run",
            "mcp",
            "run",
            SERVER_PATHS[server_name]
        ],
        env=None
    )


async def call_mcp_tool(
    server_name: str,
    tool_name: str,
    arguments: dict
):

    server_params = create_server_params(server_name)

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments
            )

            # ---------------------------------
            # Extract actual MCP response
            # ---------------------------------

            if result.content:

                first_content = result.content[0]

                # TextContent returned by MCP
                if hasattr(first_content, "text"):
                    return first_content.text

            return None