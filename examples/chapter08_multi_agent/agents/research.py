def research_agent(state):
    user_request = state["user_request"]

    print(f"Research Agent: {user_request}")

    return {
        "research_result": (
            "交通費は20,000円、"
            "ホテル代は18,000円です。"
        )
    }