from graph import graph


# Graphを実行する
result = graph.invoke(
    {
        "message": "LangGraph"
    }
)


# 最終的なStateを表示する
print(result["message"])