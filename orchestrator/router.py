from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from orchestrator.state import AgentState

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0
)


def route_question(state: AgentState):

    question = state["question"]

    prompt = f"""
You are a routing classifier for an AI assistant.

A question can require ONE or MULTIPLE sources.

Available sources:

1. database
   Use this when information is required from the company's MySQL database.

2. google_search
   Use this when information is required from the public internet,
   current market information, latest information, news, etc.

IMPORTANT:
If the question requires information from BOTH the company database
AND the public internet, select BOTH routes.

Examples:

Question:
"show me all products"

Return:
database


Question:
"what is the latest version of Python?"

Return:
google_search


Question:
"fetch products whose price is greater than 1000 and tell me
the latest market price of those products"

Return:
database,google_search


Question:
"fetch Detol products, show their descriptions, and check whether
those flavours are available in the current market"

Return:
database,google_search


Question:
"what is the difference between MCP and API?"

Return:
google_search


Question:
"how many products are in stock?"

Return:
database


USER QUESTION:

{question}

Return ONLY one of these formats:

database

google_search

database,google_search
"""

    response = llm.invoke(prompt)

    # --------------------------------
    # Extract Gemini response
    # --------------------------------

    content = response.content

    if isinstance(content, list):

        route = ""

        for item in content:

            if isinstance(item, dict):

                if "text" in item:
                    route += item["text"]

            elif isinstance(item, str):
                route += item

    else:
        route = content

    # --------------------------------
    # Clean response
    # --------------------------------

    route = route.strip().lower()

    route = route.replace("```", "")
    route = route.replace("`", "")
    route = route.strip()

    # --------------------------------
    # Determine routes
    # --------------------------------

    routes = []

    if "database" in route:
        routes.append("database")

    if "google_search" in route:
        routes.append("google_search")

    # --------------------------------
    # Validate
    # --------------------------------

    if not routes:

        raise ValueError(
            f"Invalid route returned by LLM: {route}"
        )

    print(f"\nRouter selected: {routes}")

    return {
        "routes": routes
    }