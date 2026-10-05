import asyncio

from orchestrator.graph import build_graph


async def main():

    graph = build_graph()

    question = input("\nEnter your question: ")

    result = await graph.ainvoke({
        "question": question
    })

    print("\n==============================")
    print("FINAL ANSWER")
    print("==============================")

    print(result["answer"])


if __name__ == "__main__":
    asyncio.run(main())