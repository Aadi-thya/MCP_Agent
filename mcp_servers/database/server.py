from mcp.server.fastmcp import FastMCP
from sqlalchemy import URL, create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP("LocalDatabase")


MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

print("Host:", MYSQL_HOST)
print("Port:", MYSQL_PORT)
print("User:", MYSQL_USER)
print("Database:", MYSQL_DATABASE)

database_url = URL.create(
    drivername="mysql+pymysql",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DATABASE,
)

engine = create_engine(database_url)


# -----------------------------
# MCP Tool: Get tables
# -----------------------------

@mcp.tool()
def get_tables() -> list[str]:
    """Get all tables from the local database."""

    with engine.connect() as connection:

        result = connection.execute(
            text("SHOW TABLES")
        )

        return [row[0] for row in result]


# -----------------------------
# MCP Tool: Get schema
# -----------------------------

@mcp.tool()
def get_schema() -> str:
    """Get the schema of all tables."""

    schema = ""

    with engine.connect() as connection:

        tables = connection.execute(
            text("SHOW TABLES")
        )

        for row in tables:

            table_name = row[0]

            columns = connection.execute(
                text(f"DESCRIBE `{table_name}`")
            )

            schema += f"\nTable: {table_name}\n"

            for column in columns:
                schema += (
                    f"- {column[0]} "
                    f"({column[1]})\n"
                )

    return schema


# -----------------------------
# MCP Tool: Execute SQL
# -----------------------------

@mcp.tool()
def execute_sql(sql: str) -> str:
    """Execute a read-only SQL query against the local database."""

    sql_clean = sql.strip().lower()

    forbidden = [
        "insert",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create"
    ]

    if any(sql_clean.startswith(word) for word in forbidden):
        return "Only read-only SQL queries are allowed."

    try:

        with engine.connect() as connection:

            result = connection.execute(
                text(sql)
            )

            rows = result.fetchall()

            if not rows:
                return "No results found."

            columns = result.keys()

            output = []

            output.append(
                " | ".join(columns)
            )

            output.append(
                " | ".join(["---"] * len(columns))
            )

            for row in rows:

                output.append(
                    " | ".join(
                        str(value)
                        for value in row
                    )
                )

            return "\n".join(output)

    except Exception as e:

        return f"Database error: {str(e)}"


# -----------------------------
# Start MCP server
# -----------------------------

if __name__ == "__main__":

    print(
        f"Connecting to MySQL database: "
        f"{MYSQL_DATABASE}"
    )

    # Test connection before starting MCP
    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        print(
            "Database connected successfully!"
        )

    except Exception as e:

        print(
            f"Database connection failed: {e}"
        )

        raise

    # Start MCP server
    mcp.run()