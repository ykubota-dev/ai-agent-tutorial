from langchain_core.tools import tool


# 足し算を行うTool
@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b
from langchain_core.tools import tool


# 足し算を行うTool
@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b


# 掛け算を行うTool
@tool
def multiply(a: int, b: int) -> int:
    """2つの整数を掛け算します。"""
    return a * b


# Toolの情報を確認する
print("Tool名:")
print(add.name)

print("\nToolの説明:")
print(add.description)

print("\nToolの引数:")
print(add.args)


# Toolを実行する
result = add.invoke(
    {
        "a": 10,
        "b": 20
    }
)

print("\n実行結果:")
print(result)

# 掛け算を行うTool
@tool
def multiply(a: int, b: int) -> int:
    """2つの整数を掛け算します。"""
    return a * b


# Toolの情報を確認する
print("Tool名:")
print(add.name)

print("\nToolの説明:")
print(add.description)

print("\nToolの引数:")
print(add.args)


# Toolを実行する
result = add.invoke(
    {
        "a": 10,
        "b": 20
    }
)

print("\n実行結果:")
print(result)