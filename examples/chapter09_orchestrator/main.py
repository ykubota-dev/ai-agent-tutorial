from graph import graph


result = graph.invoke(
    {
        "user_request": (
            "東京から大阪への移動方法を調べて、"
            "交通費20,000円とホテル代18,000円の"
            "合計費用も教えてください。"
        ),
        "research_result": "",
        "calculation_result": "",
        "final_answer": "",
        "route": "",
    },
    config={
        "recursion_limit": 10
    }
)


print("\nFinal Answer:")
print(result["final_answer"])