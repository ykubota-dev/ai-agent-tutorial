from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

from tools import add, multiply


# .envファイルから環境変数を読み込む
load_dotenv()


# LLMを作成する
llm = ChatOpenAI(
    model="gpt-5.5"
)


# LLMが利用できるTool
tools = [
    add,
    multiply
]


# LLMにToolを登録する
llm_with_tools = llm.bind_tools(tools)


# Tool名からToolを取得するための辞書
tools_by_name = {
    tool.name: tool
    for tool in tools
}


# User Message
messages = [
    HumanMessage(
        content="10と20を足してください。"
    )
]


# LLMへ質問する
response = llm_with_tools.invoke(messages)

messages.append(response)


# Tool Callingが行われた場合
if response.tool_calls:

    # 複数のTool Callがある場合もすべて実行する
    for tool_call in response.tool_calls:
        print("Tool Call:")
        print(tool_call)

        selected_tool = tools_by_name[tool_call["name"]]
        tool_result = selected_tool.invoke(tool_call["args"])

        print("\nTool Result:")
        print(tool_result)

        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )

    final_response = llm_with_tools.invoke(messages)
    print("\nFinal Answer:")
    print(final_response.content)

else:

    # Toolが不要な場合はLLMの回答をそのまま表示する
    print(response.content)