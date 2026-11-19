from typing import TypedDict


class AgentState(TypedDict):
    user_request: str
    research_result: str
    calculation_result: str
    final_answer: str
    route: str