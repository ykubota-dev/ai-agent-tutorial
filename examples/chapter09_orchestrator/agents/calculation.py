from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from tools.calculator import add, multiply


llm = ChatOpenAI(
    model="gpt-5.5"
)


calculation_agent_executor = create_agent(
    model=llm,
    tools=[
        add,
        multiply
    ]
)


def calculation_agent(state):
    request = f"""
ユーザーの依頼:
{state["user_request"]}

調査結果:
{state["research_result"]}

必要な計算を行ってください。
"""

    result = calculation_agent_executor.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request
                }
            ]
        }
    )

    calculation_result = (
        result["messages"][-1].content
    )

    print(
        f"Calculation Agent -> {calculation_result}"
    )

    return {
        "calculation_result": calculation_result
    }