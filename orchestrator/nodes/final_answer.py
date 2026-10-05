from orchestrator.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0
)


def final_answer_node(state: AgentState):

    print("\nGenerating final answer...")

    question = state["question"]

    routes = state.get("routes", [])

    database_result = state.get(
        "result",
        "No database information was requested."
    )

    search_result = state.get(
        "search_result",
        "No Google Search information was requested."
    )

    prompt = f"""
You are the final answer generator for an AI assistant.

USER QUESTION:
{question}

ROUTES USED:
{routes}

DATABASE RESULT:
{database_result}

GOOGLE SEARCH RESULT:
{search_result}

Instructions:

1. Answer the user's question using the available information.
2. If the question used only the database, use the DATABASE RESULT.
3. If the question used only Google Search, use the GOOGLE SEARCH RESULT.
4. If both sources were used, combine both results.
5. Do not invent information.
6. Do not claim that information exists in a source if it does not.
7. Give a clear and concise answer.

Return only the final answer.
"""

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list):

        answer = ""

        for item in content:

            if isinstance(item, dict):

                if "text" in item:
                    answer += item["text"]

            elif isinstance(item, str):
                answer += item

    else:
        answer = content

    print("\nFINAL ANSWER")
    print(answer)

    return {
        "answer": answer
    }