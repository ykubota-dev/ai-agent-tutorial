def answer_agent(state):
    research_result = state["research_result"]
    calculation_result = state["calculation_result"]

    final_answer = (
        f"{research_result}\n"
        f"{calculation_result}"
    )

    return {
        "final_answer": final_answer
    }