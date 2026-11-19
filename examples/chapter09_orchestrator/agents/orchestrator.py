from typing import Literal

from pydantic import BaseModel
from langchain_openai import ChatOpenAI


class RouteDecision(BaseModel):
    route: Literal[
        "research",
        "calculation",
        "answer",
        "end",
    ]


llm = ChatOpenAI(
    model="gpt-5.5"
)

router_llm = llm.with_structured_output(
    RouteDecision
)


def orchestrator_agent(state):
    prompt = f"""
あなたは複数のAgentへ仕事を振り分けるOrchestratorです。

ユーザーの依頼:
{state["user_request"]}

調査結果:
{state["research_result"]}

計算結果:
{state["calculation_result"]}

最終回答:
{state["final_answer"]}

次に実行する処理を1つ選択してください。

research:
調査が必要で、まだ調査結果がない場合

calculation:
計算が必要で、まだ計算結果がない場合

answer:
必要な情報が揃っていて、まだ最終回答がない場合

end:
最終回答が完成している場合

すでに完了している処理は繰り返さないでください。
"""

    decision = router_llm.invoke(prompt)

    print(
        f"Orchestrator -> {decision.route}"
    )

    return {
        "route": decision.route
    }