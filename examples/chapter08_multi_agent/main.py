from graph import graph


# Multi Agentを実行する
result = graph.invoke(
    {
        "user_request": (
            "東京から大阪へ2泊3日で旅行したいです。"
            "予算は5万円です。"
        ),
        "research_result": "",
        "calculation_result": "",
        "final_answer": ""
    }
)


# 最終回答を表示する
print("\nFinal Answer:")
print(result["final_answer"])