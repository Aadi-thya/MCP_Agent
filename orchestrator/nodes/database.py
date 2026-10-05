from orchestrator.mcpclient import call_mcp_tool
from orchestrator.sql_generator import generate_sql
from orchestrator.state import AgentState

from orchestrator.schema_cache import (
    get_schema_from_cache,
    save_schema_to_cache
)


async def get_schema_node(state: AgentState):

    print("\nChecking schema cache...")

    # Check cache first
    schema = get_schema_from_cache()

    if schema is not None:

        print("Using schema from cache...")

    else:

        print("Schema not found in cache.")
        print("Fetching schema from Database MCP...")

        schema = await call_mcp_tool(
            "database",
            "get_schema",
            {}
        )

        # Save schema into cache
        save_schema_to_cache(schema)

        print("Schema saved to cache.")

    return {
        "schema": schema
    }


def generate_sql_node(state: AgentState):

    question = state["question"]
    schema = state["schema"]

    print("\nGenerating SQL...")

    sql = generate_sql(
        question,
        schema
    )

    print("Generated SQL:")
    print(sql)

    return {
        "sql": sql
    }


async def execute_sql_node(state: AgentState):

    sql = state["sql"]

    print("\nExecuting SQL through Database MCP...")

    result = await call_mcp_tool(
        "database",
        "execute_sql",
        {
            "sql": sql
        }
    )

    return {
        "result": result
    }