from langgraph.graph import StateGraph, START, END

from state import AgentState
from agents.research import research_agent
from agents.calculation import calculation_agent
from agents.answer import answer_agent


# Graphを作成する
builder = StateGraph(AgentState)


# AgentをNodeとして登録する
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


# Agentの実行順序を設定する
builder.add_edge(
    START,
    "research"
)

builder.add_edge(
    "research",
    "calculation"
)

builder.add_edge(
    "calculation",
    "answer"
)

builder.add_edge(
    "answer",
    END
)


# Graphを完成させる
graph = builder.compile()