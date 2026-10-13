from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model="gpt-5.5"
)


def answer_agent(state):
    prompt = f"""
ユーザーの依頼:
{state["user_request"]}

調査結果:
{state["research_result"]}

計算結果:
{state["calculation_result"]}

これらの情報を使って、
ユーザーへの最終回答を作成してください。
"""

    response = llm.invoke(prompt)

    print(
        f"Answer Agent -> {response.content}"
    )

    return {
        "final_answer": response.content
    }