from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from tools.search import search


llm = ChatOpenAI(
    model="gpt-5.5"
)


research_agent_executor = create_agent(
    model=llm,
    tools=[
        search
    ]
)


def research_agent(state):
    result = research_agent_executor.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": state["user_request"]
                }
            ]
        }
    )

    research_result = (
        result["messages"][-1].content
    )

    print(
        f"Research Agent -> {research_result}"
    )

    return {
        "research_result": research_result
    }