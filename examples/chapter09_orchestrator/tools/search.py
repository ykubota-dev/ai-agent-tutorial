from langchain_core.tools import tool


@tool
def search(query: str) -> str:
    """指定された内容について情報を検索します。"""

    return (
        f"{query}について調査しました。"
        "東京から大阪へは新幹線で移動できます。"
        "交通費は20,000円、ホテル代は18,000円です。"
    )