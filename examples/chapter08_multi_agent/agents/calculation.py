def calculation_agent(state):
    research_result = state["research_result"]

    print(f"Calculation Agent: {research_result}")

    return {
        "calculation_result": (
            "合計費用は38,000円です。"
        )
    }