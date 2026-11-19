from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """2つの整数を掛け算します。"""
    return a * b