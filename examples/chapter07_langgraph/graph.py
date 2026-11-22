from langgraph.graph import StateGraph, START, END

from state import GraphState


# messageの先頭に「Hello」を付けるNode
def hello_node(state: GraphState):
    name = state["message"]

    return {
        "message": f"Hello {name}"
    }


# messageを大文字にするNode
def upper_node(state: GraphState):
    message = state["message"]

    return {
        "message": message.upper()
    }


# Graphを作成する
builder = StateGraph(GraphState)


# Nodeを登録する
builder.add_node(
    "hello",
    hello_node
)

builder.add_node(
    "upper",
    upper_node
)


# Edgeを設定する
builder.add_edge(
    START,
    "hello"
)

builder.add_edge(
    "hello",
    "upper"
)

builder.add_edge(
    "upper",
    END
)


# Graphを完成させる
graph = builder.compile()
