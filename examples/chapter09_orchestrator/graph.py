from langgraph.graph import StateGraph, START, END

from state import AgentState

from agents.orchestrator import orchestrator_agent
from agents.research import research_agent
from agents.calculation import calculation_agent
from agents.answer import answer_agent


# 完了済みの処理が再選択されていないか確認する
def route_next(state):
    route = state["route"]

    completed_routes = {
        "research": bool(state["research_result"]),
        "calculation": bool(state["calculation_result"]),
        "answer": bool(state["final_answer"]),
    }

    if route in completed_routes and completed_routes[route]:
        raise ValueError(
            f"完了済みの処理が再選択されました: {route}"
        )

    return route


# Graphを作成する
builder = StateGraph(AgentState)


# AgentをNodeとして登録する
builder.add_node(
    "orchestrator",
    orchestrator_agent
)

builder.add_node(
    "research",
    research_agent
)

builder.add_node(
    "calculation",
    calculation_agent
)

builder.add_node(
    "answer",
    answer_agent
)


# 最初はOrchestratorへ進む
builder.add_edge(
    START,
    "orchestrator"
)


# Orchestratorの判断によって
# 次に実行するAgentを変更する
builder.add_conditional_edges(
    "orchestrator",
    route_next,
    {
        "research": "research",
        "calculation": "calculation",
        "answer": "answer",
        "end": END,
    },
)


# 各Agentの処理後は
# Orchestratorへ戻る
builder.add_edge(
    "research",
    "orchestrator"
)

builder.add_edge(
    "calculation",
    "orchestrator"
)

builder.add_edge(
    "answer",
    "orchestrator"
)


# Graphを完成させる
graph = builder.compile()