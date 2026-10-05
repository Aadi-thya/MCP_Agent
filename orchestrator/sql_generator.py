from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0
)


def generate_sql(question: str, schema: str) -> str:

    prompt = f"""
You are an expert MySQL SQL developer.

You are given the database schema below.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

Generate the SQL query required to answer the user's question.

Rules:

1. Generate ONLY MySQL SQL.
2. Do not use markdown.
3. Do not use ```sql.
4. Do not explain the query.
5. Use only tables and columns that exist in the schema.
6. For products, use the table `product`.
7. For categories, use the table `category`.
8. Do not generate INSERT.
9. Do not generate UPDATE.
10. Do not generate DELETE.
11. Do not generate DROP.
12. Do not generate ALTER.
13. Do not generate TRUNCATE.
14. Only generate SELECT queries.

Return only the SQL query.
"""

    response = llm.invoke(prompt)

    content = response.content

    # Handle Gemini returning a list
    if isinstance(content, list):

        sql = ""

        for item in content:

            if isinstance(item, dict) and "text" in item:
                sql += item["text"]

            elif isinstance(item, str):
                sql += item

    else:

        sql = content

    sql = sql.strip()

    # Remove markdown fences if returned
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql